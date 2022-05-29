//
//  Helping.swift
//  Bohour_iOS
//
//  Created by Omar on 25/05/2022.
//

import Foundation
import SwiftUI

extension Color {
    
    //grays
    static let gray_1 = Color(red: 0.95, green: 0.95, blue: 0.95)
    static let gray_2 = Color(red: 0.90, green: 0.90, blue: 0.90)
    static let gray_3 = Color(red: 0.80, green: 0.80, blue: 0.80)
    static let gray_4 = Color(red: 0.70, green: 0.70, blue: 0.70)
    static let gray_5 = Color(red: 0.60, green: 0.60, blue: 0.60)
    static let gray_6 = Color(red: 0.50, green: 0.50, blue: 0.50)
    static let gray_7 = Color(red: 0.40, green: 0.40, blue: 0.40)
    static let gray_8 = Color(red: 0.30, green: 0.30, blue: 0.30)
    static let gray_9 = Color(red: 0.20, green: 0.20, blue: 0.20)
    static let gray_10 = Color(red: 0.10, green: 0.10, blue: 0.10)
    
    //selected pallete
    static let myPallete = pallete_1
    
    //pallete colors
    static let myPrimary = myPallete["primary"]!
    static let mySecondary = myPallete["secondary"]!
    static let myDark = myPallete["dark"]!
    static let myLight = myPallete["light"]!
    
    //all color palletes
    static let pallete_1 = ["primary":Color(hex: "417D7A"),
                     "secondary":Color(hex: "1D5C63"),
                     "dark":Color(hex: "1A3C40"),
                     "light":Color(hex: "EDE6DB")]
}

extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (1, 1, 1, 0)
        }

        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue:  Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

extension StringProtocol {
    subscript(offset: Int) -> Character {
        self[index(startIndex, offsetBy: offset)]
    }
}

///////// METHODS ////////

func readLocalFile(forName name: String) -> Data? {
    do {
        if let bundlePath = Bundle.main.path(forResource: name,
                                             ofType: "json"),
            let jsonData = try String(contentsOfFile: bundlePath).data(using: .utf8) {
            return jsonData
        }
    } catch {
        print(error)
    }
    
    return nil
}

func parse(jsonData: Data) -> Response? {
    do {
        let decodedData = try JSONDecoder().decode(Response.self,from: jsonData)
        return decodedData
    } catch {
        print("decode error")
        return nil
    }
}
