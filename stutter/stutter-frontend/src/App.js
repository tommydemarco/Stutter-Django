//importing useEffect and useState hooksin in order to make requests to the API
import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';

//looking up tweets
function loadTweets(callback) {
  const xhr = new XMLHttpRequest()
  const method = 'GET' // "POST"
  const url = "http://127.0.0.1:8000/api/posts/"
  const responseType = "json"
  xhr.responseType = responseType
  xhr.open(method, url)
  xhr.onload = function() {
      callback(xhr.response, xhr.status)
      console.log(xhr.response)
  }
  xhr.onerror = function (e) {
    console.log(e)
    callback({'message':'the request was an error'}, 400)
  }
      //tweetsElement.innerHTML = finalTweetStr
  xhr.send()
}

function Tweet(props){
  const {tweet} = props
  return (
    <div className="col-md-12 my-2">
      <p>{tweet.content} from {tweet.user}</p>
    </div>
  )
}

function App() {
  const [tweets, setTweet] = useState([])

  useEffect(() => {
    //defining the callback for the XHR function above
    const myCallback = (response, status) => {
      if (status === 200) {
        setTweet(response)
      } else {
        console.log('something went terribly wrong')
      }
    }
    loadTweets(myCallback)  
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>Tweets</h2>
        {/* looping trough the tweets */}
        {tweets.map((individual_tweet, index) => {
          return <Tweet tweet={individual_tweet} key={index} />
        })}
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
