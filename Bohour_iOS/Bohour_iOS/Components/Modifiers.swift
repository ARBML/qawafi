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
                    .stroke(Color.myLight, lineWidth: 1)
            }
            .background(
                Color.white
                    .cornerRadius(8)
                    .shadow(color: Color.myLight.opacity(0.7), radius: 8, x: 0, y: 8)
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

struct ButtonModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .frame(minHeight:54)
            .frame(maxWidth:.infinity)
            .background(Color.myPrimary)
            .foregroundColor(.white)
            .cornerRadius(8)
    }
}


