import torch
print(torch.cuda.is_available())  # Devuelve True si CUDA está disponible, es decir, si tienes una GPU compatible.
print(torch.cuda.device_count())  # Número de GPUs disponibles


if torch.cuda.is_available():
    print(f"Versión de CUDA disponible: {torch.version.cuda}")
    print(torch.cuda.get_device_name(0))  # Nombre de la primera GPU
else:
    print("No hay GPU disponible.")

if torch.cuda.is_available():
    print(f"Memoria total de la GPU: {torch.cuda.get_device_properties(0).total_memory / (1024 ** 3):.2f} GB")
    print(f"Memoria usada en la GPU: {torch.cuda.memory_allocated(0) / (1024 ** 3):.2f} GB")
    print(f"Memoria libre en la GPU: {torch.cuda.memory_reserved(0) / (1024 ** 3):.2f} GB")
else:
    print("No hay GPU disponible.")

# Crear un tensor y moverlo a la GPU (si está disponible)
tensor = torch.randn(3, 3)
if torch.cuda.is_available():
    tensor = tensor.to('cuda')  # Mover tensor a GPU
else:
    tensor = tensor.to('cpu')  # Mantener tensor en CPU

# Verificar si el tensor está en la GPU o en la CPU
print(f'Tensor está en: {tensor.device}')

torch.cuda.empty_cache()
