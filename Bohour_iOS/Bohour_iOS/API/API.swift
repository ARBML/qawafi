//
//  API.swift
//  Bohour_iOS
//
//  Created by Omar on 06/05/2022.
//

import Foundation


class API {
    
    static func getResults(part_1: String, part_2:String) async throws -> Response? {
        
        //body
        struct JsonData: Codable { let name,job: String }
        let jsonDataModel = JsonData(name: part_1, job: part_2)
        let jsonData = try? JSONEncoder().encode(jsonDataModel)
        
        //prep request
        let url = URL(string: "https://reqres.in/api/users")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type") // the request is JSON
        request.setValue("application/json", forHTTPHeaderField: "Accept") // the response expected to be in JSON format
        request.httpBody = jsonData
        
        //run
        let (data, _) = try await URLSession.shared.data(for: request, delegate: nil)
        if let decodedResponse = try? JSONDecoder().decode(Response.self, from: data) {
            return decodedResponse
        }
        
        return nil
        
    }
}
