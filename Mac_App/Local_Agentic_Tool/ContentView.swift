import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = ContentViewModel()

    var body: some View {
        // Main ZStack to hold the gradient background and the chat content
        ZStack {
            // Flashy gradient background for the whole window
            LinearGradient(
                gradient: Gradient(colors: [Color(red: 0.1, green: 0.1, blue: 0.25), Color(red: 0.2, green: 0.15, blue: 0.35)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 0) {
                headerView
                chatScrollView
                messageInputView
            }
        }
        .frame(minWidth: 450, idealWidth: 600, minHeight: 500, idealHeight: 700)
    }

    // The header view with an icon and styled title
    private var headerView: some View {
        HStack(spacing: 12) {
            Image(systemName: "brain.head.profile.fill")
                .font(.title)
                .foregroundColor(.cyan)
            
            Text("RAG AI Assistant")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.white)
            
            Spacer()
        }
        .padding()
        .background(.black.opacity(0.2)) // A subtle background to lift it off the gradient
    }

    // The scrollable list of chat messages
    private var chatScrollView: some View {
        ScrollViewReader { scrollViewProxy in
            ScrollView {
                VStack(spacing: 16) { // Increased spacing for a cleaner look
                    ForEach(viewModel.messages) { message in
                        MessageView(message: message)
                    }
                }
                .padding()
            }
            .onChange(of: viewModel.messages) { _ in
                if let lastMessage = viewModel.messages.last {
                    withAnimation(.spring()) { // A bouncier animation
                        scrollViewProxy.scrollTo(lastMessage.id, anchor: .bottom)
                    }
                }
            }
        }
    }

    // The input field and send button with a "glassmorphism" effect
    private var messageInputView: some View {
        HStack(spacing: 12) {
            TextField("Ask a question...", text: $viewModel.currentInput, onCommit: viewModel.submitQuery)
                .textFieldStyle(PlainTextFieldStyle())
                .padding(12)
                .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16, style: .continuous)) // Frosted glass effect
                .foregroundColor(.white)

            Button(action: viewModel.submitQuery) {
                Image(systemName: "arrow.up.circle.fill")
                    .font(.title)
                    .foregroundColor(viewModel.canSubmit ? .cyan : .gray.opacity(0.6)) // Vibrant send color
            }
            .buttonStyle(PlainButtonStyle())
            .disabled(!viewModel.canSubmit)
            .animation(.easeInOut, value: viewModel.canSubmit) // Animate color change
        }
        .padding()
        .background(.black.opacity(0.2)) // Match the header's background
    }
}
