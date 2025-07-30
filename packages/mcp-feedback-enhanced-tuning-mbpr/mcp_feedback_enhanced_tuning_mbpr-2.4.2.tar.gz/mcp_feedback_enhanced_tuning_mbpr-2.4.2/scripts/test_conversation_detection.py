#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Script for AI Conversation End Detection
==============================================

Script untuk testing fitur deteksi akhir conversation AI.
"""

import sys
import os
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_feedback_enhanced.server import detect_ai_conversation_end, should_auto_trigger_feedback

def test_detection_patterns():
    """Test conversation end detection patterns"""
    print("🧪 Testing AI Conversation End Detection")
    print("=" * 50)
    
    # Test cases - should detect
    positive_cases = [
        "Would you like me to keep going?",
        "Would you like me to continue?",
        "Should I continue?",
        "Do you want me to proceed?",
        "Would you like me to proceed?",
        "Is there anything else you'd like me to help with?",
        "Is there anything else I can help you with?",
        "Let me know if you need any further assistance",
        "Feel free to ask if you need any help",
        "Let me know if you have any questions",
        # Chinese versions
        "您希望我繼續嗎？",
        "需要我繼續嗎？",
        "還有其他需要幫助的嗎？",
        "還需要其他協助嗎？",
        "如有其他問題請告訴我",
        "如果需要進一步協助請告知",
        # Mixed case and context
        "I've completed the task. Would you like me to keep going?",
        "The code is ready. SHOULD I CONTINUE with testing?",
        "Everything looks good. 需要我繼續嗎？",
    ]
    
    # Test cases - should NOT detect
    negative_cases = [
        "I am working on your request.",
        "Here is the code you requested.",
        "The task is completed successfully.",
        "Please review the changes.",
        "Let me know what you think.",
        "This is a regular message.",
        "我正在處理您的請求。",
        "這是完成的代碼。",
        "請檢查這些更改。",
    ]
    
    print("✅ Testing POSITIVE cases (should detect):")
    passed_positive = 0
    for i, case in enumerate(positive_cases, 1):
        result = detect_ai_conversation_end(case)
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {i:2d}. {status} - '{case[:50]}{'...' if len(case) > 50 else ''}'")
        if result:
            passed_positive += 1
    
    print(f"\n❌ Testing NEGATIVE cases (should NOT detect):")
    passed_negative = 0
    for i, case in enumerate(negative_cases, 1):
        result = detect_ai_conversation_end(case)
        status = "✅ PASS" if not result else "❌ FAIL"
        print(f"  {i:2d}. {status} - '{case[:50]}{'...' if len(case) > 50 else ''}'")
        if not result:
            passed_negative += 1
    
    print(f"\n📊 Results:")
    print(f"  Positive cases: {passed_positive}/{len(positive_cases)} passed")
    print(f"  Negative cases: {passed_negative}/{len(negative_cases)} passed")
    print(f"  Overall: {passed_positive + passed_negative}/{len(positive_cases) + len(negative_cases)} passed")
    
    return passed_positive == len(positive_cases) and passed_negative == len(negative_cases)

def test_auto_trigger():
    """Test auto trigger functionality"""
    print("\n🎯 Testing Auto Trigger Functionality")
    print("=" * 50)
    
    # Test with auto trigger enabled (default)
    os.environ.pop("MCP_AUTO_TRIGGER", None)  # Remove if exists
    
    test_cases = [
        ("Would you like me to keep going?", True),
        ("I am working on your request.", False),
        ("需要我繼續嗎？", True),
        ("這是完成的代碼。", False),
    ]
    
    print("🔛 Testing with MCP_AUTO_TRIGGER enabled (default):")
    passed = 0
    for case, expected in test_cases:
        result = should_auto_trigger_feedback(case)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"  {status} - '{case[:40]}{'...' if len(case) > 40 else ''}' -> {result} (expected {expected})")
        if result == expected:
            passed += 1
    
    # Test with auto trigger disabled
    os.environ["MCP_AUTO_TRIGGER"] = "false"
    
    print(f"\n🔴 Testing with MCP_AUTO_TRIGGER disabled:")
    disabled_passed = 0
    for case, expected in test_cases:
        result = should_auto_trigger_feedback(case)
        expected_disabled = False  # Should always be False when disabled
        status = "✅ PASS" if result == expected_disabled else "❌ FAIL"
        print(f"  {status} - '{case[:40]}{'...' if len(case) > 40 else ''}' -> {result} (expected {expected_disabled})")
        if result == expected_disabled:
            disabled_passed += 1
    
    # Clean up
    os.environ.pop("MCP_AUTO_TRIGGER", None)
    
    print(f"\n📊 Auto Trigger Results:")
    print(f"  Enabled mode: {passed}/{len(test_cases)} passed")
    print(f"  Disabled mode: {disabled_passed}/{len(test_cases)} passed")
    
    return passed == len(test_cases) and disabled_passed == len(test_cases)

def test_edge_cases():
    """Test edge cases"""
    print("\n🔍 Testing Edge Cases")
    print("=" * 50)
    
    edge_cases = [
        ("", False, "Empty string"),
        (None, False, "None input"),
        ("   ", False, "Whitespace only"),
        ("Would you like me to keep going? Yes, please continue.", True, "Pattern with additional text"),
        ("WOULD YOU LIKE ME TO KEEP GOING?", True, "All caps"),
        ("would you like me to keep going?", True, "All lowercase"),
        ("  Would you like me to keep going?  ", True, "With whitespace"),
    ]
    
    passed = 0
    for i, (case, expected, description) in enumerate(edge_cases, 1):
        try:
            result = detect_ai_conversation_end(case)
            status = "✅ PASS" if result == expected else "❌ FAIL"
            print(f"  {i}. {status} - {description}: {result} (expected {expected})")
            if result == expected:
                passed += 1
        except Exception as e:
            print(f"  {i}. ❌ ERROR - {description}: {e}")
    
    print(f"\n📊 Edge Cases Results: {passed}/{len(edge_cases)} passed")
    return passed == len(edge_cases)

def main():
    """Main test function"""
    print("🎯 MCP Feedback Enhanced Tuning MBPR - Conversation Detection Tests")
    print("=" * 70)
    
    # Enable debug mode for testing
    os.environ["MCP_DEBUG"] = "true"
    
    all_passed = True
    
    # Run all tests
    tests = [
        ("Detection Patterns", test_detection_patterns),
        ("Auto Trigger", test_auto_trigger),
        ("Edge Cases", test_edge_cases),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*70}")
        try:
            results[test_name] = test_func()
            all_passed = all_passed and results[test_name]
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with error: {e}")
            results[test_name] = False
            all_passed = False
    
    # Final summary
    print(f"\n{'='*70}")
    print("🏁 FINAL RESULTS")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
    print(f"\n🎯 Overall: {overall_status}")
    
    # Clean up
    os.environ.pop("MCP_DEBUG", None)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
