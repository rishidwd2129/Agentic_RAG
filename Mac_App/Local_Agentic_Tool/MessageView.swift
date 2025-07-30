//
//  MessageView.swift
//  Local_Agentic_Tool
//
//  Created by Rishi Dwivedi on 21/07/25.
//

import SwiftUI

struct MessageView: View {
    let message: Message
    
    var body: some View {
        HStack {
            // User messages align to the right
            if message.isFromUser {
                Spacer()
            }
            
            VStack(alignment: .leading, spacing: 4) {
                // The main message text content
                Text(message.text)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
                    .background(bubbleColor)
                    .foregroundColor(textColor)
                    .cornerRadius(16)
                    .textSelection(.enabled)
                
                // Show a small "Bot" or "You" label
                Text(message.isFromUser ? "You" : "AI_Agent")
                    .font(.caption)
                    .foregroundColor(.gray)
                    .padding(.leading, 8)
            }
            .id(message.id) // Add ID for ScrollViewReader
            
            // Bot messages align to the left
            if !message.isFromUser {
                Spacer()
            }
        }
    }
    
    // Determine bubble color based on sender and error state
    private var bubbleColor: Color {
        if message.isError {
            return Color.red.opacity(0.8)
        }
        return message.isFromUser ? .accentColor : Color(.textBackgroundColor)
    }
    
    // Determine text color for readability
    private var textColor: Color {
        if message.isError {
            return .white
        }
        return message.isFromUser ? .white : Color(.textColor)
    }
}
