export default class APIService{
  static RunMCS(data){
    return fetch(`http://localhost:5000/run-mcs`,{
            'method':'POST',
             headers : {
            'Content-Type':'application/json'
      },
      body:JSON.stringify(data)
    })
    .then(response => response.json())
    .catch(error => console.log(error))
  }

  static RunBL(data){
    return fetch(`http://localhost:5000/run-bl`,{
      'method':'POST',
      headers : {
        'Content-Type':'application/json'
      },
      body:JSON.stringify(data)
    })
    .then(response => response.json())
    .catch(error => console.log(error))
  }
}
