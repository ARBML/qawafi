//
//  HsitoryView.swift
//  Qawafi
//
//  Created by Omar Hammad on 5/29/22.
//

import SwiftUI

struct HistoryView: View {
    
    @Environment(\.presentationMode) var presentationMode
    
    @ObservedObject var previousItems:PreviousResults
    @State var selectedItem:ResponseNew? = nil
    
    var body: some View {
        ZStack(alignment:.top){
            
            //close
            Capsule()
                .frame(width: 50, height: 10)
                .foregroundColor(Color.gray_1)
                .padding(.top)
            
            VStack(alignment: .leading, spacing:8){
                Text("تحليلات سابقة")
                    .font(.system(size: 28, weight: .black))
                Text("اختر أحد التحليلات لإظهار النتائج السابقة")
                    .foregroundColor(Color.gray_6)
                ScrollView{
                    VStack(alignment:.leading){
                        ForEach(0..<previousItems.items.count, id:\.self){ i in
                            CardView(items: $previousItems.items, selectedItem: $selectedItem, i: i)
                        }
                    }
                }
            }
            .padding()
            .padding(.top,32)
            .onChange(of: previousItems.items, perform: { newValue in
                if newValue.count == 0 {
                    presentationMode.wrappedValue.dismiss()
                }
            })
            .sheet(item: $selectedItem) {
            } content: { response in
                ResultsView(response: response)
                    .environment(\.layoutDirection, .rightToLeft)
                    .environment(\.locale,.init(identifier: "ar"))
                    .preferredColorScheme(.light)
            }
        }
    }
    
}

struct HistoryView_Previews: PreviewProvider {
    static var previews: some View {
        HistoryView(previousItems: PreviousResults.getSample())
            .environment(\.layoutDirection, .rightToLeft)
    }
}

struct CardView: View {
    
    @Binding var items:[ResponseNew]
    @Binding var selectedItem:ResponseNew?
    var i:Int
    
    var body: some View {
        
        //text
        Button {
            self.selectedItem = items[i]
        } label: {
            Text(combineBaits(items[i].diacritized))
            .font(.system(size: 14))
            .bold()
            .lineSpacing(8)
            .truncationMode(.tail)
            .frame(maxWidth:.infinity,alignment: .leading)
            .multilineTextAlignment(.leading)
            .frame(maxHeight:72)
            .padding()
            .background(Color.myPrimary)
            .cornerRadius(12)
            .foregroundColor(.myLight)
            .shadow(color: .myLight.opacity(0.7), radius: 12, x: 0, y: 8)
            
        }
        
    }
    
    
    func combineBaits(_ string:[String]) -> String {
        return string.reduce("", { partialResult, str in
            partialResult + "\n" + str
        })
        .replacingOccurrences(of: "#", with: "  ")
        .trimmingCharacters(in: .whitespacesAndNewlines)
    }
}
