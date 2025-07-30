# Changelog - MCP Feedback Enhanced Tuning MBPR

## [2.4.0] - 2024-12-19

### 🎯 Major Features

#### 🤖 AI Conversation End Detection
- **Smart Detection**: Automatically detects AI conversation ending phrases
  - English patterns: "Would you like me to keep going?", "Should I continue?", etc.
  - Chinese patterns: "您希望我繼續嗎？", "需要我繼續嗎？", etc.
- **Auto Trigger**: Automatically opens MCP feedback when conversation end is detected
- **Configurable Control**: New `MCP_AUTO_TRIGGER` environment variable
  - Set to `true` (default) to enable auto-triggering
  - Set to `false` to disable auto-triggering

#### ⏱️ Extended Timeout
- **40% Increase**: Default timeout extended from 600 seconds to 840 seconds (14 minutes)
- **Better UX**: More time for users to provide thoughtful feedback
- **Consistent**: Applied across all components (GUI, Web UI, MCP server)

#### 🔧 Enhanced Package Management
- **New Package Name**: `mcp-feedback-enhanced-tuning-mbpr`
- **Conflict Avoidance**: Prevents conflicts with original package
- **Updated Scripts**: All entry points updated to new package name

### 🛠️ Technical Improvements

#### 📋 Configuration Updates
- **MCP Configuration**: Updated examples for new package name
- **Environment Variables**: Added `MCP_AUTO_TRIGGER` documentation
- **README Updates**: Comprehensive documentation updates

#### 🔍 Detection Logic
- **Pattern Matching**: Robust pattern matching for conversation end detection
- **Case Insensitive**: Works regardless of text case
- **Multi-language**: Supports both English and Chinese patterns
- **Debug Logging**: Detailed logging for detection events

### 📚 Documentation

#### 📖 Updated Documentation
- **Installation Guide**: Updated with new package name
- **Configuration Examples**: All examples use new package name
- **Environment Variables**: Added documentation for new variables
- **Feature Description**: Detailed explanation of new features

#### 🎯 Usage Examples
```json
{
  "mcpServers": {
    "mcp-feedback-enhanced-tuning-mbpr": {
      "command": "uvx",
      "args": ["mcp-feedback-enhanced-tuning-mbpr@latest"],
      "timeout": 600,
      "env": {
        "MCP_AUTO_TRIGGER": "true"
      },
      "autoApprove": ["interactive_feedback"]
    }
  }
}
```

### 🔄 Migration Guide

#### From Original Package
1. **Update MCP Configuration**:
   - Change package name from `mcp-feedback-enhanced` to `mcp-feedback-enhanced-tuning-mbpr`
   - Update all `uvx` commands to use new package name

2. **Environment Variables**:
   - Add `MCP_AUTO_TRIGGER=true` to enable auto-detection (optional, enabled by default)

3. **Testing**:
   - Test with: `uvx mcp-feedback-enhanced-tuning-mbpr@latest test`

### 🎉 Benefits

#### 🚀 Improved Workflow
- **Seamless Integration**: AI conversations flow more naturally
- **Reduced Manual Intervention**: Auto-detection reduces need for manual MCP calls
- **Better Timing**: Extended timeout allows for more thoughtful responses

#### 🎯 Enhanced User Experience
- **Intelligent Detection**: System knows when to ask for feedback
- **Flexible Control**: Users can disable auto-detection if needed
- **Consistent Behavior**: Works across all interface types (GUI/Web)

### 🔧 Technical Details

#### Detection Patterns
```python
end_patterns = [
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
    "如果需要進一步協助請告知"
]
```

#### Timeout Changes
- **Server Default**: 600s → 840s (+40%)
- **GUI Config**: 600s → 840s (+40%)
- **Documentation**: Updated all references

### 🏷️ Version Information
- **Version**: 2.4.0
- **Package Name**: mcp-feedback-enhanced-tuning-mbpr
- **Release Date**: 2024-12-19
- **Compatibility**: Maintains full backward compatibility with existing features

---

**Note**: This is a tuned version of the original MCP Feedback Enhanced with specific improvements for AI conversation flow and user experience.
