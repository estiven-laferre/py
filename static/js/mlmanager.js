// mlmanager.js

var ML = function(params){

	this.key2translations = {};
	this.keys = []
	if(params.hasOwnProperty('key2translations')){
		this.key2translations = params.key2translations;
		this.keys = Object.keys(this.key2translations);
	}

	this.t = function(k){
		if(this.keys.indexOf(k) === -1){
			alert('key = '  +  k  +  ' not found');
			return;
		}
		s = this.key2translations[k];
		return s.replace(/"/g,'\"');
	};
};