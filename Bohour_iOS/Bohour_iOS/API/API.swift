//
//  API.swift
//  Bohour_iOS
//
//  Created by Omar on 06/05/2022.
//

import Foundation


class API {
    
    static func getResults(_ text: String) async throws -> ResponseNew? {
        
        //body
        struct JsonData: Codable { let baits:String }
        let jsonDataModel = JsonData(baits: text)
        let jsonData = try? JSONEncoder().encode(jsonDataModel)
        
        //prep request
        let url = URL(string: "https://92c3-170-133-89-186.eu.ngrok.io/api/analyze")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type") // the request is JSON
        request.setValue("application/json", forHTTPHeaderField: "Accept") // the response expected to be in JSON format
        request.httpBody = jsonData
        
        //run
        do {
            let (data, resp) = try await URLSession.shared.data(for: request, delegate: nil)
            
            if let httpResponse = resp as? HTTPURLResponse {
                    print("statusCode: \(httpResponse.statusCode)")
            }
            
            if let decodedResponse = try? JSONDecoder().decode(ResponseNew.self, from: data) {
                print("decooded")
                return decodedResponse
            }else{
                print("cannot decooded")
            }
        }catch{
            print(error)
        }
        
        return nil
        
    }
    
    static func getAnalysis(_ text: String) async throws -> ResponseNew? {
        
        //prep request
        let parameters = [
          [
            "key": "baits",
            "value": text,
            "type": "text"
          ]] as [[String : Any]]

        let boundary = "Boundary-\(UUID().uuidString)"
        var body = ""
        
        for param in parameters {
          if param["disabled"] == nil {
            let paramName = param["key"]!
            body += "--\(boundary)\r\n"
            body += "Content-Disposition:form-data; name=\"\(paramName)\""
            if param["contentType"] != nil {
              body += "\r\nContent-Type: \(param["contentType"] as! String)"
            }
            let paramType = param["type"] as! String
            if paramType == "text" {
              let paramValue = param["value"] as! String
              body += "\r\n\r\n\(paramValue)\r\n"
            } else {
              let paramSrc = param["src"] as! String
              let fileData = try NSData(contentsOfFile:paramSrc, options:[]) as Data
              let fileContent = String(data: fileData, encoding: .utf8)!
              body += "; filename=\"\(paramSrc)\"\r\n"
                + "Content-Type: \"content-type header\"\r\n\r\n\(fileContent)\r\n"
            }
          }
        }
        
        body += "--\(boundary)--\r\n";
        let postData = body.data(using: .utf8)

        var request = URLRequest(url: URL(string: "https://12c0-170-133-89-186.eu.ngrok.io/api/analyze")!,timeoutInterval: Double.infinity)
        request.addValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        request.httpMethod = "POST"
        request.httpBody = postData
        
        //run
        do {
            let (data, resp) = try await URLSession.shared.data(for: request, delegate: nil)
            
            if let httpResponse = resp as? HTTPURLResponse {
                    print("statusCode: \(httpResponse.statusCode)")
            }
            
            if let decodedResponse = try? JSONDecoder().decode(ResponseNew.self, from: data) {
                print("decooded")
                return decodedResponse
            }else{
                print("cannot decooded")
            }
        }catch{
            print(error)
        }
        
        return nil
        
    }
}
