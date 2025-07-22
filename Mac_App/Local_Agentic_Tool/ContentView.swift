import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = ContentViewModel()
    
    var body: some View {
        VStack(spacing: 0) {
            headerView
            chatScrollView
            Divider()
            messageInputView // This is now correctly in scope
        }
        .background(Color(.windowBackgroundColor))
        .frame(minWidth: 450, idealWidth: 600, minHeight: 500, idealHeight: 700)
    }
    
    // The header view
    private var headerView: some View {
        HStack {
            Text("RAG AI Assistant")
                .font(.title2)
                .fontWeight(.semibold)
            Spacer()
        }
        .padding()
        .background(Color(.windowBackgroundColor).shadow(radius: 2))
    }
    
    // The scrollable list of chat messages
    private var chatScrollView: some View {
        ScrollViewReader { scrollViewProxy in
            ScrollView {
                VStack(spacing: 12) {
                    ForEach(viewModel.messages) { message in
                        MessageView(message: message)
                    }
                }
                .padding()
            }
            .onChange(of: viewModel.messages) { _ in
                if let lastMessage = viewModel.messages.last {
                    withAnimation {
                        scrollViewProxy.scrollTo(lastMessage.id, anchor: .bottom)
                    }
                }
            }
        }
    }
    
    // The input field and send button at the bottom
    private var messageInputView: some View {
        HStack(spacing: 12) {
            TextField("Ask a question...", text: $viewModel.currentInput, onCommit: viewModel.submitQuery)
                .textFieldStyle(PlainTextFieldStyle())
                .padding(10)
                .background(Color(.textBackgroundColor))
                .cornerRadius(12)
            
            Button(action: viewModel.submitQuery) {
                Image(systemName: "arrow.up.circle.fill")
                    .font(.title)
            }
            .buttonStyle(PlainButtonStyle())
            .foregroundColor(viewModel.canSubmit ? .accentColor : .gray)
            .disabled(!viewModel.canSubmit)
        }
        .padding()
    }
} // <-- The closing brace for ContentView is here, ensuring all helper views are inside.
