import timm
import torch
import coremltools as ct

model_name = "mobileclip_b_lt_timm"

model = timm.create_model(
    f"hf_hub:apple/{model_name}", pretrained=True, exportable=True
)
model.eval()

example_input = torch.rand(1, 3, 224, 224)
traced_model = torch.jit.trace(model, example_input)

model_from_trace = ct.convert(
    traced_model,
    inputs=[ct.TensorType(shape=example_input.shape)],
)

model_from_trace.save(f"{model_name}.mlpackage")
