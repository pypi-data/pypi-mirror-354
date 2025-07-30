#!/usr/bin/env python3
"""
Demo script for Thai QR Payment with Gaming feature
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import thaiqrpayment

def demo():
    print("Thai QR Payment - Gaming Feature Demo")
    print("=" * 40)
    
    # Sample QR code data (replace with actual data)
    test_code = "00020101021129370016A000000677010111011300660000000005802TH5303764540510.006304"
    
    print("\n1. Generating regular QR code...")
    thaiqrpayment.save(test_code, "/tmp/demo_regular_qr.png")
    print("✓ Regular QR saved to: /tmp/demo_regular_qr.png")
    
    print("\n2. Generating Gaming QR code with 'Online Gaming Only' text...")
    thaiqrpayment.save_gaming_qr(test_code, "/tmp/demo_gaming_qr.png")
    print("✓ Gaming QR saved to: /tmp/demo_gaming_qr.png")
    
    print("\n3. Generating QR code with custom text...")
    thaiqrpayment.save(test_code, "/tmp/demo_custom_qr.png", insert_text="Custom Text Example")
    print("✓ Custom QR saved to: /tmp/demo_custom_qr.png")
    
    print("\n4. Generating base64 gaming QR...")
    base64_str = thaiqrpayment.gaming_qr_to_base64(test_code)
    print(f"✓ Base64 gaming QR generated (length: {len(base64_str)})")
    
    print("\nDemo completed! Check the generated files in /tmp/")
    print("\nUsage examples:")
    print("# Regular QR")
    print("thaiqrpayment.save(code, 'output.png')")
    print("")
    print("# Gaming QR with 'Online Gaming Only' text")
    print("thaiqrpayment.save_gaming_qr(code, 'gaming.png')")
    print("")
    print("# Custom text QR")
    print("thaiqrpayment.save(code, 'custom.png', insert_text='Your Text')")

if __name__ == "__main__":
    demo()
