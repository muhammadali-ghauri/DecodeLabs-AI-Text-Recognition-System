import cv2
import pytesseract
import os

print("========================================")
print("        AI Text Recognition System")
print("========================================")

# Ask user for image filename
filename = input("\nEnter image filename: ").strip()

# Create complete image path
image_path = os.path.join("images", filename)

# Check whether the image exists
if not os.path.exists(image_path):
    print("\nError: Image file not found.")
else:
    # Read the image
    image = cv2.imread(image_path)

    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply Otsu thresholding
    _, processed_image = cv2.threshold(
        blurred_image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Extract text from processed image
    text = pytesseract.image_to_string(processed_image)

    # Get OCR data including confidence scores
    data = pytesseract.image_to_data(
        processed_image,
        output_type=pytesseract.Output.DICT
    )

    # Store valid confidence scores
    confidence_scores = []

    for confidence in data["conf"]:
        confidence = float(confidence)

        if confidence >= 0:
            confidence_scores.append(confidence)

    # Calculate average confidence
    if confidence_scores:
        average_confidence = sum(confidence_scores) / len(confidence_scores)
    else:
        average_confidence = 0

    # Display results
    print("\n========================================")
    print("          OCR Recognition Result")
    print("========================================")

    print("\nExtracted Text:")
    print(text)

    print(f"Average Confidence: {average_confidence:.2f}%")

    # Validate confidence threshold
    if average_confidence >= 80:
        print("Status: Recognition Successful")
    else:
        print("Status: Confidence Below 80%")

    # Create unique output filename
    name_without_extension = os.path.splitext(filename)[0]
    output_path = os.path.join(
        "output",
        f"{name_without_extension}_processed.png"
    )

    # Save processed image
    cv2.imwrite(output_path, processed_image)

    print(f"\nProcessed image saved as: {output_path}")