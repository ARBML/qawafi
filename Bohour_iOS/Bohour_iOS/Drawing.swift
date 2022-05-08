//
//  Drawing.swift
//  Bohour_iOS
//
//  Created by Omar on 07/05/2022.
//

import SwiftUI

struct BadgeBackground: View {
    
    @State var start = 0
    @State var end:Double = 360
    @State var step:Double = 1
    @State var a:CGFloat = 2
    @State var size:CGFloat = 10
    
    var body: some View {
        
        ZStack(alignment: .bottom){
            //Drawing
            GeometryReader { geometry in
                
                let centerX = geometry.size.width/2
                let centerY = geometry.size.height/2
                
                Path { path in
                    
                    // go to center
                    path.move(to: CGPoint(x: centerX, y: centerY))
                    
                    //ellipses
                    let angles = stride(from: Double(start), to: Double(end), by: step)
                    
                    angles.forEach { ang in
                        let angle = CGFloat(ang)
                        let x = centerX + a * angle * cos(angle)
                        let y = centerY + a * angle * sin(angle)
                        path.addEllipse(in: CGRect(x: x, y: y, width: size, height: size))
                    }
                    
                }
                .fill(.linearGradient(
                    Gradient(colors: [Self.gradientStart, Self.gradientEnd]),
                    startPoint: UnitPoint(x: 0.5, y: 0),
                    endPoint: UnitPoint(x: 0.5, y: 0.6)
                ))
                .blendMode(.multiply)
            }
            .drawingGroup()
            .frame(maxHeight:.infinity)
            .ignoresSafeArea(.all)
            
            //controls
            VStack{
                HStack{
                    Text("A")
                    Slider(
                        value: $a,
                        in: 0...10
                    )
                    Text("\(a, specifier: "%.1f")")
                }
                
                HStack{
                    Text("Size")
                    Slider(
                        value: $size,
                        in: 0...100
                    )
                    Text("\(size, specifier: "%.1f")")
                }
                
                HStack{
                    Text("Steps")
                    Slider(
                        value: $end,
                        in: 0...2000
                    )
                    Text("\(end, specifier: "%.1f")")
                }
                
                HStack{
                    Text("Density")
                    Slider(
                        value: $step,
                        in: 0...1
                    )
                    Text("\(step, specifier: "%.2f")")
                }
                
            }
            .tint(.black)
            .padding()
        }
        .onAppear {
            
            var sign = -1.0
            var stepSign = -1.0
                        
            Timer.scheduledTimer(withTimeInterval: 0.05, repeats: true) { t in
                
                //end += 1
                //a -= 0.01
                //size += 0.1*sign
                step -= 0.001*stepSign
                                
                if Int(size.truncatingRemainder(dividingBy: 10)) == 0 {
                    sign *= -1.0
                }
                
                if step == 0 {
                    stepSign *= -1.0
                }
            }
        }
    
    }
    
    static let gradientStart = Color(red: 239.0 / 255, green: 120.0 / 255, blue: 221.0 / 255)
    static let gradientEnd = Color(red: 239.0 / 255, green: 172.0 / 255, blue: 120.0 / 255)
}

struct BadgeBackground_Previews: PreviewProvider {
    static var previews: some View {
        BadgeBackground()
    }
}

struct HexagonParameters {
    
    struct Segment {
        let line: CGPoint
        let curve: CGPoint
        let control: CGPoint
    }

    static let adjustment: CGFloat = 0.1

    static let segments = [
        Segment(
            line:    CGPoint(x: 0.60, y: 0.05),
            curve:   CGPoint(x: 0.40, y: 0.05),
            control: CGPoint(x: 0.50, y: 0.00)
        ),
        Segment(
            line:    CGPoint(x: 0.05, y: 0.20 + adjustment),
            curve:   CGPoint(x: 0.00, y: 0.30 + adjustment),
            control: CGPoint(x: 0.00, y: 0.25 + adjustment)
        ),
        Segment(
            line:    CGPoint(x: 0.00, y: 0.70 - adjustment),
            curve:   CGPoint(x: 0.05, y: 0.80 - adjustment),
            control: CGPoint(x: 0.00, y: 0.75 - adjustment)
        ),
        Segment(
            line:    CGPoint(x: 0.40, y: 0.95),
            curve:   CGPoint(x: 0.60, y: 0.95),
            control: CGPoint(x: 0.50, y: 1.00)
        ),
        Segment(
            line:    CGPoint(x: 0.95, y: 0.80 - adjustment),
            curve:   CGPoint(x: 1.00, y: 0.70 - adjustment),
            control: CGPoint(x: 1.00, y: 0.75 - adjustment)
        ),
        Segment(
            line:    CGPoint(x: 1.00, y: 0.30 + adjustment),
            curve:   CGPoint(x: 0.95, y: 0.20 + adjustment),
            control: CGPoint(x: 1.00, y: 0.25 + adjustment)
        )
    ]
}
