import SwiftUI

struct MessageView: View {
    let message: Message
    
    var body: some View {
        HStack {
            // User messages align to the right
            if message.isFromUser {
                Spacer(minLength: 50) // Ensure bubbles don't stretch full-width
            }
            
            VStack(alignment: message.isFromUser ? .trailing : .leading, spacing: 5) {
                // The main message text content with a gradient background
                Text(message.text)
                    .padding(.horizontal, 16)
                    .padding(.vertical, 10)
                    .background(bubbleGradient) // Apply the new gradient
                    .foregroundColor(.white)
                    .clipShape(RoundedRectangle(cornerRadius: 20, style: .continuous)) // Smoother corners
                    .textSelection(.enabled)
                
                // Show a small "Bot" or "You" label with an icon for the AI
                HStack(spacing: 4) {
                    if !message.isFromUser {
                        Image(systemName: "sparkles") // AI icon
                            .font(.caption2)
                    }
                    Text(message.isFromUser ? "You" : "AI Agent")
                }
                .font(.caption)
                .foregroundColor(.gray)
                .padding(.horizontal, 8)
            }
            .id(message.id)
            
            // Bot messages align to the left
            if !message.isFromUser {
                Spacer(minLength: 50)
            }
        }
    }
    
    // Determine bubble gradient based on sender and error state
    @ViewBuilder
    private var bubbleGradient: some View {
        if message.isError {
            LinearGradient(
                gradient: Gradient(colors: [.red, .orange]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        } else if message.isFromUser {
            LinearGradient(
                gradient: Gradient(colors: [.blue, .purple]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        } else {
            // A sleek, dark bubble for the AI
            Color.black.opacity(0.4)
        }
    }
}
