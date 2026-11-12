import React,{useState,useEffect} from 'react';
import Header from '../Header/Header';
import {api} from '../../api';
export default function Login(){
 const [error,setError]=useState('');
 useEffect(()=>{api('/djangoapp/session');},[]);
 async function submit(e){e.preventDefault();try{const r=await api('/djangoapp/login',Object.fromEntries(new FormData(e.target)));sessionStorage.setItem('username',r.userName);window.location.href='/';}catch(err){setError(err.message);}}
 return <><Header/><main className="narrow"><p className="eyebrow">WELCOME BACK</p><h1>Log in to Best Cars</h1><form onSubmit={submit}><label>Username<input name="userName" autoComplete="username" required/></label><label>Password<input type="password" name="password" autoComplete="current-password" required/></label><p role="alert">{error}</p><button>Login</button></form><p>New here? <a href="/register">Register now</a></p></main></>;
}
