from vietnamese_address_parser import __version__

def main():
    # Print static banner without calling Hello
    print(f"Vietnamese Address Parser v{__version__}")
    print("Hello! Welcome to the Vietnamese Address Parser CLI.")
    print("Usage example:")
    print("    parser = VietnameseAddressParser()")
    print("    result = parser('54-55 Bau Cat 4, Phuong 14, Tan Binh, Ho Chi Minh')")
    print("    print(result)")
    print("⚠️   NOTE  ⚠️:")
    print("This parser uses the OpenStreetMap Nominatim API for geolocation enhancement.")
    print("As a result, some lookups may take a few seconds due to network latency or rate limits.")