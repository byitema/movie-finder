import UIKit

class ViewController: UIViewController,UICollectionViewDataSource,UICollectionViewDelegate {
    struct GlobalVariable{
        static var InfoList = NSDictionary();
    }
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        GlobalVariable.InfoList.count;
    }
    
    @IBOutlet weak var ViewCollection: UICollectionView!
    
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView
            .dequeueReusableCell(withReuseIdentifier: "MyCell", for: indexPath) as! MovieCell;
        
        // let movieInfo = (MainViewController.GlobalVariable.MOVIES.object(forKey: ((MainViewController.GlobalVariable.MOVIES.allKeys ) [indexPath.row]))) as! NSDictionary;
        var movieInfo=MainViewController.GlobalVariable.MOVIES[indexPath.row] as! NSDictionary
        //print(movieInfo)
        //print(MainViewController.GlobalVariable.jsonDict)
        //print(MainViewController.GlobalVariable.MOVIES)
        
        // Configure the cell
        cell.layer.borderColor = UIColor.orange.cgColor
        cell.layer.borderWidth = 3
        
        cell.Name.text = movieInfo.object(forKey: "movie_name") as! String
        let tmp = movieInfo.object(forKey: "movie_year") as! NSNumber;
        cell.Year.text = "Year: \(tmp.description)"
        
        let tmp1 = movieInfo.object(forKey: "rating") as! NSNumber;
        cell.Rating.text = "Rating: \(tmp1.description)"
        
        let tmp2 = movieInfo.object(forKey: "genre") as! String;
        cell.Genre.text = "Genre: \(tmp2.description)"
        
        return cell
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        
        let filePath = Bundle.main.path(forResource: "MovieInfo", ofType: "plist")
        GlobalVariable.InfoList = NSDictionary(contentsOfFile:filePath!)!
        print(MainViewController.GlobalVariable.jsonDict)
        print(MainViewController.GlobalVariable.MOVIES)
    }
    
    
    // page controlling
    @IBOutlet var PageNumberTextField: UILabel!
    
    @IBAction func LeftButtonPressed(_ sender: Any) {
        var pageNumber = Int(PageNumberTextField.text!)!
        if pageNumber > 1 {
            pageNumber -= 1
            PageNumberTextField.text = "\(pageNumber)"
            
            MainViewController.GlobalVariable.MOVIES = NSMutableOrderedSet()
            MainViewController.GlobalVariable.jsonDict = NSDictionary()
            getMovies()
            do{
                sleep(2)
            }
            
            var index = 0
            for (genre, movies ) in MainViewController.GlobalVariable.jsonDict {
                //print(genre)
                for movie in (movies as! NSArray) {
                    //print(movie)
                    MainViewController.GlobalVariable.MOVIES[index] = movie
                    index += 1
                }
            }
            var indexPathsNeedToReload = [IndexPath]()

            for cell in ViewCollection.visibleCells {
              let indexPath: IndexPath = ViewCollection.indexPath(for: cell)!

                indexPathsNeedToReload.append(indexPath)
              
            }

            ViewCollection.reloadItems(at: indexPathsNeedToReload)
        }
    }
    
    @IBAction func RightButtonPressed(_ sender: Any) {
        var pageNumber = Int(PageNumberTextField.text!)!
        if !MainViewController.GlobalVariable.MOVIES.isEqual(to: NSOrderedSet()) {
            pageNumber += 1
            PageNumberTextField.text = "\(pageNumber)"
            
            MainViewController.GlobalVariable.MOVIES = NSMutableOrderedSet()
            MainViewController.GlobalVariable.jsonDict = NSDictionary()
            getMovies()
            do{
                sleep(2)
            }
            var index = 0
            for (genre, movies ) in MainViewController.GlobalVariable.jsonDict {
                //print(genre)
                for movie in (movies as! NSArray) {
                    //print(movie)
                    MainViewController.GlobalVariable.MOVIES[index] = movie
                    index += 1
                }
            }
            var indexPathsNeedToReload = [IndexPath]()

            for cell in ViewCollection.visibleCells {
              let indexPath: IndexPath = ViewCollection.indexPath(for: cell)!

                indexPathsNeedToReload.append(indexPath)
              
            }

            ViewCollection.reloadItems(at: indexPathsNeedToReload)
        }
        
    }
    
    func getMovies(){
    
        // prepare json data
        let json: [String: Any] = ["genres": MainViewController.GlobalVariable.genres, "year_from": MainViewController.GlobalVariable.year_from, "year_to": MainViewController.GlobalVariable.year_to, "regexp": MainViewController.GlobalVariable.title, "top_number": 4]

        let jsonData = try? JSONSerialization.data(withJSONObject: json)

        // create post request
        let url = URL(string: ("https://eee33e85c2df.ngrok.io/" + "\(Int(PageNumberTextField.text!)!)"))!
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
                MainViewController.GlobalVariable.jsonDict = responseJSON as NSDictionary
            }
        }

        task.resume()
    }
    
    
}

