// This file was generated from JSON Schema using quicktype, do not modify it directly.
// To parse the JSON, add this file to your project and do:
//
//   let response = try? newJSONDecoder().decode(Response.self, from: jsonData)

import Foundation

// MARK: - Response
class ResponseNew: Identifiable, Codable, Equatable  {
    
            
    let diacritized: [String]
    let arudi_style: [[String]]
    let qafiyah: [String]
    let meter: String
    let era: [String]
    let closest_patterns: [[ClosestPattern]]
    let theme: [String]

    static func getSample() -> ResponseNew? {
        if let data = readLocalFile(forName: "resp") {
            let res = parseLocal(jsonData: data)
            return res
        }else{
            print("not loaded")
            return nil
        }
    }
    
    static func parseLocal(jsonData: Data) -> ResponseNew? {
        do {
            let decodedData = try JSONDecoder().decode(ResponseNew.self,from: jsonData)
            return decodedData
        } catch {
            print("decode error")
            return nil
        }
    }
    
    static func == (lhs: ResponseNew, rhs: ResponseNew) -> Bool {
        return lhs.diacritized == rhs.diacritized
    }
}

enum ClosestPattern: Codable {
    
    case double(Double)
    case string(String)

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if let x = try? container.decode(Double.self) {
            self = .double(x)
            return
        }
        if let x = try? container.decode(String.self) {
            self = .string(x)
            return
        }
        throw DecodingError.typeMismatch(ClosestPattern.self, DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Wrong type for ClosestPattern"))
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        switch self {
        case .double(let x):
            try container.encode(x)
        case .string(let x):
            try container.encode(x)
        }
    }
    
}
