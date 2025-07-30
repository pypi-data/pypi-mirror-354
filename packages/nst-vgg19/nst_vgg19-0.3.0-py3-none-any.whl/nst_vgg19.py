import numpy as np
import torch
import torch.nn as nn
from torch.optim import LBFGS
import torch.nn.functional as F

class ContentLoss(nn.Module):
    def __init__(self):
        super(ContentLoss, self).__init__()
        self.target = None
        self.target_mul = 1

    def forward(self, input):
        if self.target is not None:
            self.loss = F.mse_loss(input, self.target * self.target_mul)
        return input
    
    def set_target_feature(self, target_feature):
        self.target = target_feature.detach()
    
    def reset_target(self):
        self.target = None
        
    def set_target_mul(self, mul: float):
        self.target_mul = mul

class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = self.gram_matrix(target_feature).detach()
        self.target_mul = 1

    def forward(self, input):
        G = self.gram_matrix(input)
        self.loss = F.mse_loss(G, self.target * self.target_mul)

        return input
    
    def set_target_mul(self, mul: float):
        self.target_mul = mul

    @staticmethod
    def gram_matrix(input):
        a, b, c, d = input.size()
        features = input.view(a * b, c * d)  # Flatten the feature map
        G = torch.mm(features, features.t())  # Compute Gram matrix
        return G.div((a * b * c * d) ** 0.5)  # Normalize the Gram matrix
    
class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = mean.clone().detach().view(-1, 1, 1)
        self.std = std.clone().detach().view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std  # Normalize the image

class NST_VGG19:
    """
    Neural Style Transfer using VGG19.
    :param style_image: Numpy array (H, W, C) or tensor of the style image.
    :param style_layers_weights: Dictionary of weights for style losses.
    """
    def __init__(self, 
        style_image: np.ndarray | torch.Tensor, 
        style_layers=['conv_2', 'conv_4', 'conv_6', 'conv_7', 'conv_9'], 
        content_layers=['conv_6', 'conv_7'],
        gaussian_kernel_size = 3,
        gaussian_force=1.0
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if isinstance(style_image, np.ndarray):
            style_image_tensor = self.image_to_tensor(style_image)
        elif isinstance(style_image, torch.Tensor):
            style_image_tensor = style_image.clone().detach().to(self.device)
        else:
            raise TypeError("Input must be a numpy array or torch tensor.")

        self.model, self.style_losses, self.content_losses = self.build_model(
            self.device,
            style_image_tensor,
            style_layers,
            content_layers
        )
        self.model.eval()
        
        # create gaussian kernel
        ax = torch.linspace(-(gaussian_kernel_size // 2), gaussian_kernel_size // 2, gaussian_kernel_size)
        xx, yy = torch.meshgrid(ax, ax, indexing='ij')
        kernel = torch.exp(-(xx**2 + yy**2) / (2 * gaussian_force**2))
        kernel /= kernel.sum()  # norm
        kernel = kernel.unsqueeze(0).unsqueeze(0)  # batches
        self.gaussian_kernel = kernel.to(self.device)
        self.gaussian_kernel_size = gaussian_kernel_size

    def image_to_tensor(self, numpy_image):
        image_tensor = torch.from_numpy(numpy_image).permute(2, 0, 1).float().div(255) # Convert (H, W, C) to (C, H, W)
        return image_tensor.unsqueeze(0).to(self.device).contiguous()

    def tensor_to_image(self, tensor):
        img = tensor.squeeze(0).permute(1, 2, 0).clip(0, 1).mul(255).cpu().detach().numpy().astype("uint8")
        return img

    @staticmethod
    def build_model(device, style_image_tensor, style_layers, content_layers):
        # torchvision's vgg19 trained on ImageNet dataset that uses normalized images, so we need to normalize too
        normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
        normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)

        from torchvision.models import vgg19
        base_net = vgg19(weights='DEFAULT').features.to(device)
        model = nn.Sequential()
        model.add_module('normalization', Normalization(normalization_mean, normalization_std).to(device))

        style_losses = []
        content_losses = []
        i = 0

        for layer in base_net.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = f'conv_{i}'
            elif isinstance(layer, nn.ReLU):
                name = f'relu_{i}'
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = f'pool_{i}'
            elif isinstance(layer, nn.BatchNorm2d):
                name = f'bn_{i}'
            else:
                raise RuntimeError(f'Unrecognized layer: {layer.__class__.__name__}')

            model.add_module(name, layer)

            # Model does N layers then calc loss for N layers, then does other M layers and calc loss to N+M layers...

            if name in style_layers:
                target_feature = model(style_image_tensor).detach()
                style_loss = StyleLoss(target_feature)
                model.add_module(f"style_loss_{i}", style_loss)
                style_losses.append(style_loss)
            
            if name in content_layers:
                target_feature = model(style_image_tensor).detach()
                content_loss = ContentLoss()
                model.add_module(f"content_loss_{i}", content_loss)
                content_losses.append(content_loss)

        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], (StyleLoss, ContentLoss)):
                break

        model = model[:(i + 1)]

        return model, style_losses, content_losses

    def set_content_losses(self, content_image_tensor, mul: float):
        target = content_image_tensor.clone().detach()

        for module in self.model:
            if isinstance(module, ContentLoss):
                module.reset_target()
            target = module(target).detach()
            if isinstance(module, ContentLoss):
                module.set_target_feature(target)
                module.set_target_mul(mul)
    
    def set_style_target_muls(self, mul: float):
        for module in self.model:
            if isinstance(module, StyleLoss):
                module.set_target_mul(mul)
    
    def gaussian_blur(self, img):
        batch_size, channels, height, width = img.shape
        blurred = F.conv2d(
            img.view(batch_size * channels, 1, height, width), 
            self.gaussian_kernel, 
            padding=self.gaussian_kernel_size // 2
        )
        blurred = blurred.view(batch_size, channels, height, width)

        return blurred
    
    @staticmethod
    def describe_noise_level(noise_val):
        levels = ['trsh', 'bad', 'poor', 'fair', 'good', 'best']
        thresholds = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 0]
        for i, threshold in enumerate(thresholds):
            if noise_val >= threshold:
                return levels[i]
    
    def __call__(
            self, 
            content_image: np.ndarray | torch.Tensor,
            num_steps=100,
            weights=[1e-6, 5e-7, 1e-5, 1e-5, 1e-6],
            content_weights = [1e-3, 1e-3],
            output_type="np",
            label=None
        ):
        if isinstance(content_image, np.ndarray):
            input_img = self.image_to_tensor(content_image)
        elif isinstance(content_image, torch.Tensor):
            input_img = content_image.clone().detach().to(self.device)
        else:
            raise TypeError("Input must be a numpy array or torch tensor.")

        k = 4 / ((num_steps + 20) ** 0.2)
        fix = 28 / (num_steps ** 1.2) * 100
        self.set_content_losses(input_img, k)
        self.set_style_target_muls(k)
        
        optimizer = LBFGS([input_img.requires_grad_()], max_iter=num_steps)

        if label is not None:
            from tqdm import tqdm
            progress_bar = tqdm(total=num_steps, desc=label)
        
        def transfer():
            optimizer.zero_grad(set_to_none=True)

            self.model(input_img)

            total_loss = torch.tensor(0.0, device=self.device)
            
            for i, sl in enumerate(self.style_losses):
                loss = sl.loss * weights[i]
                total_loss += loss
            
            for i, cl in enumerate(self.content_losses):
                loss = cl.loss * content_weights[i]
                total_loss += loss
            
            noise_penalty = (torch.relu(-input_img).mean() + torch.relu(input_img - 1).mean())
            total_loss += noise_penalty * fix
            
            blurred = self.gaussian_blur(input_img)
            diff = torch.abs(blurred - input_img)
            diff_max = diff.max(dim=1, keepdim=True)[0]
            noise_loss = (diff_max * 7) ** 2 # если умножить на M, то фильтр (0..1)**N уменьшит 1/M разниц и увеличит (M-1)/M разниц
            noise_loss = noise_loss.mean()
            total_loss += noise_loss * k
            
            if progress_bar is not None:
                progress_bar.set_postfix(q=self.describe_noise_level(noise_penalty.item() + noise_loss.item() * 1e-3))
                progress_bar.update()

            total_loss.backward()
            return total_loss

        try:
            optimizer.step(transfer)
        except torch.OutOfMemoryError as e:
            print('torch.OutOfMemoryError')
            
        if output_type == 'np':
            return self.tensor_to_image(input_img)
        else:
            return input_img.detach()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Neural style transfer.")
    parser.add_argument("image", help="Content image.")
    parser.add_argument("-s", "--style", required=True, help="Style image.")
    parser.add_argument("-n", "--num_steps", default=100, type=int, help="More steps - more deep transfer.")
    parser.add_argument("-o", "--output", default="nst_result.png", help="Output image name.")
    args = parser.parse_args()

    import cv2
    
    init_image = cv2.imread(args.image)  # Загрузка через OpenCV
    cv2.cvtColor(init_image, cv2.COLOR_BGR2RGB, init_image)  # Преобразование BGR -> RGB

    style_image = cv2.imread(args.style)  # Загрузка через OpenCV
    cv2.cvtColor(style_image, cv2.COLOR_BGR2RGB, style_image)  # Преобразование BGR -> RGB

    nst = NST_VGG19(style_image)
    result = nst(init_image, num_steps=int(args.num_steps), label=args.image)

    cv2.imwrite(args.output, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
    
if __name__ == "__main__":
    main()
    
