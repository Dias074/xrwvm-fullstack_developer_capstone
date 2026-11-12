import React,{useEffect,useState} from 'react';
import {api} from '../../api';
export default function Header(){
 const [username,setUsername]=useState(null);
 useEffect(()=>{api('/djangoapp/session').then(x=>{setUsername(x.userName); if(x.userName)sessionStorage.setItem('username',x.userName);else sessionStorage.removeItem('username');});},[]);
 async function logout(e){e.preventDefault();await api('/djangoapp/logout',{});sessionStorage.clear();window.location.href='/';}
 return <header><a className="brand" href="/">BEST CARS</a><nav><a href="/">Dealerships</a><a href="/about">About Us</a><a href="/contact">Contact Us</a></nav><div>{username?<><strong>{username}</strong> <a href="/" onClick={logout}>Log out</a></>:<><a href="/login">Log in</a><a href="/register">Sign up</a></>}</div></header>;
}
