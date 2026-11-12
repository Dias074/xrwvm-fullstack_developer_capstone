import React,{useState,useEffect} from 'react';
import {useParams} from 'react-router-dom';
import Header from '../Header/Header';
import {api} from '../../api';
export default function Dealer(){
 const {id}=useParams();const [dealer,setDealer]=useState({}),[reviews,setReviews]=useState([]),[user,setUser]=useState(null),[error,setError]=useState('');
 useEffect(()=>{api('/djangoapp/dealer/'+id).then(x=>setDealer(x.dealer[0])).catch(e=>setError(e.message));api('/djangoapp/reviews/dealer/'+id).then(x=>setReviews(x.reviews)).catch(e=>setError(e.message));api('/djangoapp/session').then(x=>setUser(x.userName));},[id]);
 return <><Header/><main><a href="/">Back to dealerships</a><h1>{dealer.full_name}</h1><p>{dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}</p>{user&&<a className="button" href={'/postreview/'+id}>Review Dealer</a>}<h2>Customer reviews</h2><p role="alert">{error}</p><div className="cards">{reviews.map(r=><article key={r.id}><span className={'badge '+r.sentiment}>{r.sentiment}</span><p>{r.review}</p><strong>{r.name}</strong><p>{r.car_make} {r.car_model} {r.car_year} · {r.purchase_date}</p></article>)}</div>{!reviews.length&&!error&&<p>No reviews yet.</p>}</main></>;
}
