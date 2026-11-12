export async function api(url, data) {
  const token=decodeURIComponent(document.cookie.split('; ').find(x=>x.startsWith('csrftoken='))?.split('=')[1] || '');
  const response=await fetch(url,{credentials:'same-origin',method:data===undefined?'GET':'POST',headers:{'Content-Type':'application/json','X-CSRFToken':token},...(data===undefined?{}:{body:JSON.stringify(data)})});
  const result=await response.json();
  if(!response.ok) throw new Error(result.error || 'Request failed');
  return result;
}
