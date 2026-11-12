import React,{useState,useEffect} from 'react';
import {useParams} from 'react-router-dom';
import Header from '../Header/Header';
import {api} from '../../api';
export default function PostReview(){
 const {id}=useParams();const [dealer,setDealer]=useState({}),[cars,setCars]=useState([]),[error,setError]=useState('');
 useEffect(()=>{api('/djangoapp/session').then(x=>{if(!x.userName)window.location.href='/login';});api('/djangoapp/dealer/'+id).then(x=>setDealer(x.dealer[0]));api('/djangoapp/get_cars').then(x=>setCars(x.CarModels));},[id]);
 async function submit(e){e.preventDefault();const form=Object.fromEntries(new FormData(e.target));const car=cars.find(c=>String(c.id)===form.car);try{await api('/djangoapp/add_review',{...form,dealership:Number(id),car_make:car.CarMake,car_model:car.CarModel,purchase:true});window.location.href='/dealer/'+id;}catch(err){setError(err.message);}}
 return <><Header/><main className="narrow"><p className="eyebrow">SHARE YOUR EXPERIENCE</p><h1>Review {dealer.full_name}</h1><form onSubmit={submit}><label>Your review<textarea name="review" rows="5" required maxLength="5000"/></label><label>Purchase Date<input type="date" name="purchase_date" required max={new Date().toISOString().slice(0,10)}/></label><label>Car Make and Model<select name="car" required defaultValue=""><option value="" disabled>Choose a vehicle</option>{cars.map(c=><option key={c.id} value={c.id}>{c.CarMake} {c.CarModel}</option>)}</select></label><label>Car Year<input type="number" name="car_year" min="2015" max="2026" required/></label><p role="alert">{error}</p><button>Post Review</button></form></main></>;
}
