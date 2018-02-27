// A canvas for users to write

class DrawCanvas {
    // init the canvas 
    constructor(myCanvas) {
        myCanvas.drawCanvas = this;
        
        this.mouseDown = false;
        this.mouseMoved = false;
        
        this.ctx = myCanvas.getContext("2d");        
        this.ctx.strokeStyle = "#000000";

        this.boundingRect = myCanvas.getBoundingClientRect();
        
        
        myCanvas.addEventListener('mousedown', this.penDown.bind(this));
        myCanvas.addEventListener('mousemove', this.penMove.bind(this));         
        myCanvas.addEventListener('mouseup', this.penUp.bind(this));
        
        myCanvas.addEventListener('touchstart', this.penDown.bind(this));
        myCanvas.addEventListener('touchmove', this.penMove.bind(this));         
        myCanvas.addEventListener('touchend', this.penUp.bind(this));
        
    }
    
    getXY(evt) {
        let x=0, y=0;
        if (evt.clientX) {
            x = parseInt( (evt.clientX - this.boundingRect.x) / 10);
            y = parseInt( (evt.clientY - this.boundingRect.y) / 10);
        } else if (evt.changedTouches) {
            x = parseInt( (evt.changedTouches[0].clientX - this.boundingRect.x) / 10) ;
            y = parseInt( (evt.changedTouches[0].clientY - this.boundingRect.y) / 10) ;
        }
        console.log(x, y, evt);
        return [x, y];
    }

    clear() {
        this.ctx.clearRect(0,0,28,28);
    }
    
    penDown(evt) {
        evt.preventDefault();
        const xy = this.getXY(evt);
        const x = xy[0];
        const y = xy[1];
        //console.log("mouse down", x, y);
        this.clear();
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.mouseDown = true;
        this.penDownCallback ? this.penDownCallback.call() : null;        
    }
    
    penMove(evt) {
        const xy = this.getXY(evt);
        const x = xy[0];
        const y = xy[1];
        //console.log("mouse move", x, y, evt);             
        if (this.mouseDown) {
            this.mouseMoved = true;
            this.ctx.lineTo(x, y);
            this.ctx.stroke();
        }
    }

    penUp(evt) {
        const xy = this.getXY(evt);
        const x = xy[0];
        const y = xy[1];
        this.mouseDown = false;
        this.mouseMoved = false;
        this.penUpCallback ? this.penUpCallback.call() : null;
    }

    onPenUp(fun) {
        this.penUpCallback = fun;
    }
    onPenDown(fun) {
        this.penDownCallback = fun;
    }

    getImageData() {
        let data = this.ctx.getImageData(0,0,28,28);

        let imgData = data.data.filter( (d, i) => (i+1) % 4 == 0);
        let imgFloatData = Float32Array.from(imgData);

        imgFloatData.forEach( (d, i) => imgFloatData[i] = d/128);

        return imgFloatData;
    }
}

