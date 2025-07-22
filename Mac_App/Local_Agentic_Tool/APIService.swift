import Foundation
class APIService {
    private let apiURL = URL(string: "http://127.0.0.1:8000/api/query")!
    
    func performQuery(prompt: String) async throws -> String {
        var request = URLRequest(url: apiURL)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONEncoder().encode(QueryRequest(prompt: prompt))
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard (response as? HTTPURLResponse)?.statusCode == 200 else {
            // Try to decode an error message from the server if possible
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let detail = json["detail"] as? String {
                throw NSError(domain: "APIError", code: (response as? HTTPURLResponse)?.statusCode ?? 500, userInfo: [NSLocalizedDescriptionKey: detail])
            }
            throw URLError(.badServerResponse)
        }
        
        let queryResponse = try JSONDecoder().decode(QueryResponse.self, from: data)
        return queryResponse.answer
    }
}
