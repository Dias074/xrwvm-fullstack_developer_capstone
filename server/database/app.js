const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const app = express();
app.use(express.json({limit:'32kb'}));
const Reviews = require('./review');
const Dealers = require('./dealership');
const wrap = fn => (req,res,next) => Promise.resolve(fn(req,res,next)).catch(next);
app.get('/',(req,res)=>res.json({status:'ok',service:'dealerships'}));
app.get('/fetchReviews',wrap(async(req,res)=>res.json(await Reviews.find().lean())));
app.get('/fetchReviews/dealer/:id',wrap(async(req,res)=>res.json(await Reviews.find({dealership:Number(req.params.id)}).lean())));
app.get('/fetchDealers',wrap(async(req,res)=>res.json(await Dealers.find().sort({id:1}).lean())));
app.get('/fetchDealers/:state',wrap(async(req,res)=>res.json(await Dealers.find({state:req.params.state}).sort({id:1}).lean())));
app.get('/fetchDealer/:id',wrap(async(req,res)=>res.json(await Dealers.find({id:Number(req.params.id)}).lean())));
const Counter=mongoose.model('Counter',new mongoose.Schema({_id:String,value:Number}));
app.post('/insert_review',wrap(async(req,res)=>{
  const data=req.body;
  if(!data.review || !data.name || !Number.isInteger(Number(data.dealership))) return res.status(400).json({error:'Invalid review'});
  if(!await Dealers.exists({id:Number(data.dealership)})) return res.status(404).json({error:'Dealer not found'});
  const count=await Counter.findOneAndUpdate({_id:'reviews'},{$inc:{value:1}},{new:true});
  const saved=await Reviews.create({...data,id:count.value});
  res.status(201).json(saved);
}));
app.use((err,req,res,next)=>res.status(err.name==='ValidationError'?400:500).json({error:err.name==='ValidationError'?'Invalid review':'Service error'}));
async function start(){
  await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/dealershipsDB');
  for(const [model,file,key] of [[Dealers,'dealerships.json','dealerships'],[Reviews,'reviews.json','reviews']]){
    const records=JSON.parse(fs.readFileSync(path.join(__dirname,'data',file),'utf8'))[key];
    if(await model.countDocuments()===0) await model.insertMany(records);
  }
  const last=await Reviews.findOne().sort({id:-1});
  await Counter.updateOne({_id:'reviews'},{$setOnInsert:{value:last?last.id:0}},{upsert:true});
  app.listen(process.env.PORT || 3030,'0.0.0.0',()=>console.log('Dealership API listening on port '+(process.env.PORT || 3030)));
}
start().catch(err=>{console.error(err.message);process.exit(1);});
