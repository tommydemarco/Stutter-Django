import {backendLookup} from '../lookup'

export function apiTweetCreate(newTweet, callback){
    backendLookup("POST", "/posts/create/", callback, {content: newTweet})
  }
  
export function apiTweetList(callback) {
    backendLookup("GET", "/posts/", callback) 
  }