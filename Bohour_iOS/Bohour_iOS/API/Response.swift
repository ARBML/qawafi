// This file was generated from JSON Schema using quicktype, do not modify it directly.
// To parse the JSON, add this file to your project and do:
//
//   let anlss = try? newJSONDecoder().decode(Anlss.self, from: jsonData)

import Foundation

class Response: Identifiable, Codable {
    
    let baits_analysis: [BaitsAnalysis]
    let meter: String
    let topic: [Era]
    let era: [Era]
    let qafiah: Qafiah
    
    static func getSample() -> Response? {
        if let data = readLocalFile(forName: "anlss") {
            let res = parse(jsonData: data)
            return res
        }else{
            print("not loaded")
            return nil
        }
    }
}

// MARK: - BaitsAnalysis
class BaitsAnalysis: Identifiable, Codable {
    let bait_diacritized, arudi_style, tafeelat, tafeelat_pattern: String
    let broken_places: [BrokenPlace]
    let closest_bait: String

}

class BrokenPlace:Codable{
    let start:Int
    let end:Int
}

class Era: Codable {
    let name:String
    let probability:Double
}

// MARK: - Qafiah
class Qafiah: Codable {
    let rawwi, type: String

}
