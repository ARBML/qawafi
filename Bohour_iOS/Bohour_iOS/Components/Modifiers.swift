//
//  Modifiers.swift
//  Bohour_iOS
//
//  Created by Omar on 25/05/2022.
//

import SwiftUI

struct TextFieldModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .cornerRadius(8)
            .font(.system(size: 18))
            .accentColor(Color.myPrimary)
            .overlay{
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.gray_1, lineWidth: 1)
            }
            .background(
                Color.white
                    .cornerRadius(8)
                    .shadow(color: Color.gray_1, radius: 10, x: 0, y: 10)
            )
            

    }
}

struct BoxModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding(20)
            .background(Color.white)
            .cornerRadius(8)
    }
}


