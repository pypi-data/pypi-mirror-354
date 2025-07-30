#!/usr/bin/env python3
"""
Test script for the new gaming QR feature
"""

import thaiqrpayment

# Test code (you can replace this with actual QR code data)
test_code = "00020101021129370016A000000677010111011300660000000005802TH5303764540510.006304"

def test_gaming_features():
    print("Testing Gaming QR Code Features...")
    
    # Test 1: Generate QR with custom text
    print("1. Generating QR with custom text...")
    try:
        img = thaiqrpayment.generate(test_code, insert_text="Online Gaming Only")
        print("✓ Custom text generation successful")
    except Exception as e:
        print(f"✗ Custom text generation failed: {e}")
    
    # Test 2: Save gaming QR
    print("2. Saving gaming QR...")
    try:
        thaiqrpayment.save_gaming_qr(test_code, "/tmp/gaming_qr_test.png")
        print("✓ Gaming QR saved to /tmp/gaming_qr_test.png")
    except Exception as e:
        print(f"✗ Gaming QR save failed: {e}")
    
    # Test 3: Generate base64 gaming QR
    print("3. Generating base64 gaming QR...")
    try:
        base64_str = thaiqrpayment.gaming_qr_to_base64(test_code)
        print(f"✓ Base64 generated (length: {len(base64_str)})")
    except Exception as e:
        print(f"✗ Base64 generation failed: {e}")
    
    # Test 4: Generate regular QR (without text)
    print("4. Generating regular QR...")
    try:
        thaiqrpayment.save(test_code, "/tmp/regular_qr_test.png")
        print("✓ Regular QR saved to /tmp/regular_qr_test.png")
    except Exception as e:
        print(f"✗ Regular QR save failed: {e}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_gaming_features()
