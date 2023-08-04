import io
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django import forms
from django.http import FileResponse, JsonResponse
from PIL import Image
from ImageCoder import encoder, decoder


class UploadFileForm(forms.Form):
    modes = [
        ('encode', 'encode'),
        ('decode', "decode")
    ]

    image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    message = forms.CharField(
        label="Message",
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    mode = forms.ChoiceField(
        choices=modes,
        label='Mode',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}))


@csrf_exempt
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.cleaned_data['message']
            mode = form.cleaned_data['mode']
            image_name = form.cleaned_data['image']

            try:
                with Image.open(request.FILES["image"]) as image:
                    if mode == 'encode':
                        if not message:
                            form.add_error('message', "Message required for encode mode.")
                            return render(request, "steganography/index.html", {"form": form})

                        encoder.encode(image, message)

                        output_stream = io.BytesIO()
                        image.save(output_stream, format=f"{image.format}")

                        response = FileResponse(io.BytesIO(output_stream.getvalue()))
                        response['Content-Disposition'] = f'attachment; filename="encoded_{image_name}"'
                        response['Content-Type'] = 'image/jpeg'

                        return response
                    elif mode == 'decode':
                        hidden_msg = decoder.decode(image)
                        form = UploadFileForm(initial=hidden_msg)
            except OSError:
                return JsonResponse({"error": f"Cannot {mode} image."})
    else:
        form = UploadFileForm()

    return render(request, "steganography/index.html", {"form": form})
