//
//  LoadingView.swift
//  Bohour_iOS
//
//  Created by Omar on 25/05/2022.
//

import SwiftUI

struct LoadingView : View {
    
    @State var activeIndex = 0
    let numRects = 6
    var color = Color.white
    
    var body : some View {
        HStack{
            ForEach(0..<numRects){i in
                RoundedRectangle(cornerRadius: 2)
                    .foregroundColor(i == activeIndex ? Color.myLight : Color.myLight.opacity(0.5))
                    .frame(width:12,height:8)
                    .scaleEffect(i == activeIndex ? 1.5 : 1)
                    .padding(.leading, i == 3 ? 8 : 0)
            }
        }
        .onAppear {
            Timer.scheduledTimer(withTimeInterval: 0.2, repeats: true) { timer in
                
                withAnimation(.spring()){
                    activeIndex += 1
                    
                    if activeIndex == numRects {
                        activeIndex = 0
                    }
                }
            }
        }
    }
}
