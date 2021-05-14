import Foundation
import UIKit

class MainViewController : UIViewController {
    
    @IBOutlet weak var FindView: UIView!
    @IBOutlet weak var TitleTextField: UITextField!
    @IBOutlet weak var GenresTextField: UITextField!
    @IBOutlet weak var YearFromTextField: UITextField!
    @IBOutlet weak var YearToTextField: UITextField!
    
    struct GlobalVariable{
        static var jsonDict = NSDictionary();
        static var MOVIES = NSMutableOrderedSet();
        static var title = String();
        static var year_from = Int();
        static var year_to = Int();
        static var genres = String();
    }
    
    override func viewDidLoad() {
       super.viewDidLoad()
    }
    
   @IBAction func FindButton(_ sender: Any) {
    GlobalVariable.MOVIES = NSMutableOrderedSet()
    GlobalVariable.jsonDict = NSDictionary()
    
       getMovies()
    do {
        sleep(2)
    }
        var index = 0
        for (genre, movies ) in GlobalVariable.jsonDict {
            //print(genre)
            for movie in (movies as! NSArray) {
                //print(movie)
                GlobalVariable.MOVIES[index] = movie
                index += 1
            }
        }
    
    if !GlobalVariable.MOVIES.isEqual(to: NSMutableOrderedSet()){
       performSegue(withIdentifier: "FromStartToMain", sender: self);
    } else {
        let refreshAlert = UIAlertController(title: "Oops..", message: "Nothing found", preferredStyle: UIAlertController.Style.alert)

        refreshAlert.addAction(UIAlertAction(title: "Ok", style: .default, handler: { (action: UIAlertAction!) in
              print("Ok Alert")
        }))

        present(refreshAlert, animated: true, completion: nil)
    }
   }
    
    func getMovies(){
        
        GlobalVariable.title = TitleTextField.text!;
        if YearFromTextField.text != ""{
            GlobalVariable.year_from = Int(YearFromTextField.text!)!;
        } else {
            GlobalVariable.year_from = 0
        }
        if YearToTextField.text != ""{
        GlobalVariable.year_to = Int(YearToTextField.text!)!
        } else {
            GlobalVariable.year_to = 5000
        }
        GlobalVariable.genres = GenresTextField.text!;
        
        // prepare json data
        let json: [String: Any] = ["genres": GlobalVariable.genres, "year_from": GlobalVariable.year_from, "year_to": GlobalVariable.year_to, "regexp": GlobalVariable.title, "top_number": 4]
        
        
        
        let jsonData = try? JSONSerialization.data(withJSONObject: json)

        // create post request
        let url = URL(string: "https://91413471fad9.ngrok.io/")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("application/json", forHTTPHeaderField: "Accept")
        
        
        // insert json data to the request
        request.httpBody = jsonData

        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            guard let data = data, error == nil else {
                print(error?.localizedDescription ?? "No data")
                return
            }
            let responseJSON = try? JSONSerialization.jsonObject(with: data, options: [])
            if let responseJSON = responseJSON as? [String: Any] {
                GlobalVariable.jsonDict = responseJSON as NSDictionary
            }
        }

        task.resume()
    }
    
}
