//
//  PreviousResults.swift
//  Qawafi
//
//  Created by Omar Hammad on 5/29/22.
//

import Foundation

class PreviousResults : ObservableObject {
    
    let encode_key = "PREVIOUS_RESULTS"
    
    @Published var items:[ResponseNew] = [] {
        didSet{
            //save locally
            if let encoded = try? JSONEncoder().encode(items){
                UserDefaults.standard.set(encoded, forKey: "PREVIOUS_RESULTS")
            }
        }
    }
    
    init(){
        if let savedItems = UserDefaults.standard.data(forKey: encode_key){
            if let decodedItems = try? JSONDecoder().decode([ResponseNew].self, from: savedItems){
                self.items = decodedItems
            }
        }
    }
    
    public static func getSample() -> PreviousResults {
        let pr = PreviousResults()
        pr.items = [ResponseNew.getSample()!, ResponseNew.getSample()!]
        return pr
    }
    
    
    
}
