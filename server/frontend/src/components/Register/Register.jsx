import React,{useState,useEffect} from 'react';
import Header from '../Header/Header';
import {api} from '../../api';
export default function Register(){
 const [error,setError]=useState('');
 useEffect(()=>{api('/djangoapp/session');},[]);
 async function submit(e){e.preventDefault();const data=Object.fromEntries(new FormData(e.target));try{const r=await api('/djangoapp/register',data);sessionStorage.setItem('username',r.userName);window.location.href='/';}catch(err){setError(err.message);}}
 return <><Header/><main className="narrow"><p className="eyebrow">JOIN THE COMMUNITY</p><h1>Create your account</h1><form onSubmit={submit}>{[['userName','Username','text'],['firstName','First Name','text'],['lastName','Last Name','text'],['email','Email','email'],['password','Password','password']].map(([name,label,type])=><label key={name}>{label}<input name={name} type={type} required minLength={type==='password'?8:1}/></label>)}<p role="alert">{error}</p><button>Register</button></form></main></>;
}
