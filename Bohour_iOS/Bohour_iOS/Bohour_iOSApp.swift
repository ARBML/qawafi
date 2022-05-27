//
//  Bohour_iOSApp.swift
//  Bohour_iOS
//
//  Created by Omar on 06/05/2022.
//

import SwiftUI

@main
struct Bohour_iOSApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
            .environment(\.layoutDirection, .rightToLeft)
            .environment(\.locale,.init(identifier: "ar"))
            .preferredColorScheme(.light)
        }
    }
}
