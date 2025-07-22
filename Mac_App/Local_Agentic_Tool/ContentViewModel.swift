import Foundation

// --- Data Models ---
// The data structures for our application are now defined here to ensure they are in scope.
struct QueryRequest: Codable {
    let prompt: String
}

struct QueryResponse: Codable {
    let answer: String
}

struct Message: Identifiable, Equatable {
    let id = UUID()
    let text: String
    let isFromUser: Bool
    var isError: Bool = false
}


@MainActor
class ContentViewModel: ObservableObject {
    @Published var messages: [Message] = []
    @Published var currentInput: String = ""
    @Published var isLoading: Bool = false
    
    private let apiService = APIService()

    var canSubmit: Bool {
        !currentInput.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty && !isLoading
    }

    func submitQuery() {
        let prompt = currentInput.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !prompt.isEmpty else { return }

        // Add the user's message to the chat
        messages.append(Message(text: prompt, isFromUser: true))
        currentInput = ""
        isLoading = true
        
        // Add a temporary loading message for the bot
        messages.append(Message(text: "...", isFromUser: false))

        Task {
            do {
                let answer = try await apiService.performQuery(prompt: prompt)
                // Replace the loading message with the actual answer
                if let index = messages.firstIndex(where: { $0.text == "..." && !$0.isFromUser }) {
                    messages[index] = Message(text: answer, isFromUser: false)
                }
            } catch {
                // Replace the loading message with an error message
                 if let index = messages.firstIndex(where: { $0.text == "..." && !$0.isFromUser }) {
                    messages[index] = Message(text: "Error: \(error.localizedDescription)", isFromUser: false, isError: true)
                }
            }
            isLoading = false
        }
    }
}
