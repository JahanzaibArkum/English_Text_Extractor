import streamlit as st
import paddleocr
from PIL import Image
import numpy as np
import io

@st.cache_resource
def load_ocr_model():
    """Loads the PaddleOCR model with angle classification and English language."""
    ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en')
    return ocr

def detect_text(image_bytes, ocr_model):
    """Detects text in the uploaded image using the provided OCR model."""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(image)
        result = ocr_model.ocr(img_array, cls=True)
        return result, image
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return [], None

def visualize_results(image, results):
    """Draws bounding boxes and text on the image."""
    try:
        from PIL import ImageDraw
        draw = ImageDraw.Draw(image)
        for region in results:
            bbox = region[0]
            text = region[1][0]
            confidence = region[1][1]
            # Draw bounding box
            draw.polygon(bbox, outline="lime", width=3)
            # Add text label with background
            text_x, text_y = bbox[0][0], bbox[0][1] - 15
            draw.rectangle((text_x - 2, text_y - 12, text_x + len(text) * 10, text_y + 2), fill="lime")
            draw.text((text_x, text_y), f"{text} ({confidence:.2f})", fill="black")
        return image
    except ImportError:
        st.warning("Pillow (PIL) needs to be installed for visualization. Run: `pip install Pillow`")
        return image

def main():
    st.title("✨ Smart English Text Extractor ✨")
    st.markdown("Upload an image to extract text with PaddleOCR.")

    uploaded_file = st.file_uploader("📸 Upload your image here...", type=["jpg", "jpeg", "png"])

    ocr_model = load_ocr_model()

    if uploaded_file is not None:
        st.subheader("Your Uploaded Image:")
        st.image(uploaded_file, caption="Let's see what text we can find!", use_column_width=True)

        with st.spinner("🔍 Extracting text..."):
            results, processed_image = detect_text(uploaded_file.read(), ocr_model)

        st.subheader("Extracted Text:")
        if results:
            expander = st.expander("Show Detailed Text Regions")
            for i, region in enumerate(results):
                bbox = region[0]
                text = region[1][0]
                confidence = region[1][1]
                expander.markdown(f"**Region {i+1}:**")
                expander.write(f"- Bounding Box: {bbox}")
                expander.write(f"- Text: **{text}**")
                expander.write(f"- Confidence: {confidence:.4f}")
                expander.markdown("---")

            if processed_image:
                st.subheader("Detected Text on Image:")
                annotated_image = visualize_results(processed_image.copy(), results)
                st.image(annotated_image, caption="Text regions highlighted.", use_column_width=True)
        else:
            st.info("😞 No text could be detected in this image.")

if __name__ == "__main__":
    main()
