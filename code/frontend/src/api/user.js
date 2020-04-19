import request from '../utils/request'
import {backend_ip} from "./config"

const pre="http://"+backend_ip+":15000";
export function follow(data) {
	return request({
		url: pre + "/relation/follow",
		method: "post",
		data
	})
}

export function cancelFollow(data){
	return request({
		url: pre + "/relation/cancelfollow",
		method: "post",
		data
	})
}

export function addUser() {
	return request({
		url: pre + "/user/add",
		method: "post"
	})
}

export function removeUser(data) {
	return request({
		url: pre + "/user/remove",
		method: "post",
		data
	})
}

export function viewFollows(data) {
	return request({
		url: pre + "/user/viewfollows",
		method: "post",
		data
	})
}

export function viewFans(data) {
	return request({
		url: pre + "/user/viewfans",
		method: "post",
		data
	})
}

export function viewProfile(data) {
	return request({
		url: pre + "/user/viewprofile",
		method: "post",
		data
	})
}

export function viewPosts(data) {
	return request({
		url: pre + "/user/viewposts",
		method: "post",
		data
	})
}

export function staticAnalyze() {
	return request({
		url: pre + "/analyze/static",
		method: "post"
	})
}
