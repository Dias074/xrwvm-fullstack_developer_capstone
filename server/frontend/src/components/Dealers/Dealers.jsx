import React,{useState,useEffect} from 'react';
import Header from '../Header/Header';
import {api} from '../../api';
export default function Dealers(){
 const [dealers,setDealers]=useState([]),[state,setState]=useState('All'),[user,setUser]=useState(null),[error,setError]=useState('');
 useEffect(()=>{api('/djangoapp/get_dealers').then(x=>setDealers(x.dealers)).catch(e=>setError(e.message));api('/djangoapp/session').then(x=>setUser(x.userName));},[]);
 const shown=state==='All'?dealers:dealers.filter(x=>x.state===state);
 return <><Header/><main><section className="hero"><p className="eyebrow">YOUR NEXT JOURNEY STARTS HERE</p><h1>Find your trusted dealership.</h1><p>Explore our locations and read honest customer reviews.</p></section><div className="toolbar"><h2>Our dealerships <small>{shown.length} locations</small></h2><label>Filter by state<select value={state} onChange={e=>setState(e.target.value)}><option value="All">All States</option>{[...new Set(dealers.map(x=>x.state))].sort().map(s=><option key={s}>{s}</option>)}</select></label></div><p role="alert">{error}</p><div className="table-wrap"><table><thead><tr><th>ID</th><th>Dealer Name</th><th>City</th><th>Address</th><th>Zip</th><th>State</th>{user&&<th>Review Dealer</th>}</tr></thead><tbody>{shown.map(d=><tr key={d.id}><td>{d.id}</td><td><a href={'/dealer/'+d.id}>{d.full_name}</a></td><td>{d.city}</td><td>{d.address}</td><td>{d.zip}</td><td>{d.state}</td>{user&&<td><a href={'/postreview/'+d.id}>Review Dealer</a></td>}</tr>)}</tbody></table></div></main></>;
}
