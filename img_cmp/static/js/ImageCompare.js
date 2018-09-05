(function ImageCompareModule(factory) {
    "use strict";

    if (typeof define === "function" && define.amd) {
        define(factory);
    }
    else if (typeof module != "undefined" && typeof module.exports != "undefined") {
        module.exports = factory();
    }
    else {
        /* jshint sub:true */
        window["ImageCompare"] = factory();
    }

})(function ImageCompareFactory() {
    var ImageCompare = function($container) {
        this.$container = $container[0]; // get DOM object
        //this.$container = document.getElementById(options.containerId);
        this.$container.className += ' cd-image-container';

        this.$origImg = document.createElement('img');
        this.$origImg.alt = 'Original Image';
        this.$origImg.src = this.$container.getAttribute('src1');
        
        this.$label4origImg = document.createElement('span');
        this.$label4origImg.className = 'cd-image-label';
        this.$label4origImg.dataset.type = 'original';
        this.$label4origImg.textContent = 'Original';

        this.$container.appendChild(this.$origImg);
        this.$container.appendChild(this.$label4origImg);

        this.$topImgLayer = document.createElement('div');
        this.$topImgLayer.className = 'cd-resize-img';
        this.$modifiedImg = document.createElement('img');
        this.$modifiedImg.alt = 'Modified Image';
        this.$modifiedImg.src = this.$container.getAttribute('src2');
        this.$topImgLayer.appendChild(this.$modifiedImg);

        this.$label4modifiedImg = document.createElement('span');
        this.$label4modifiedImg.className = 'cd-image-label';
        this.$label4modifiedImg.dataset.type = 'modified';
        this.$label4modifiedImg.textContent = 'Modified';
        this.$topImgLayer.appendChild(this.$label4modifiedImg); 
        this.$container.appendChild(this.$topImgLayer);

        this.$moveHandler = document.createElement('span');
        this.$moveHandler.className = 'cd-handle cd-first';
        this.$container.appendChild(this.$moveHandler);

        this.dragging = false; 
        this.bindEvents();
    }
    
    ImageCompare.prototype = {
        constructor: ImageCompare,
        bindEvents: function() {
            this.drags($(this.$moveHandler), $(this.$topImgLayer), $(this.$container), $(this.$label4origImg), $(this.$label4modifiedImg));
        },

        drags: function(dragElement, resizeElement, container, labelContainer, labelResizeElement) {
            dragElement.on("mousedown vmousedown", function(e) {
                dragElement.addClass('draggable');
                resizeElement.addClass('resizable');
    
                var dragWidth = dragElement.outerWidth(),
                    xPosition = dragElement.offset().left + dragWidth - e.pageX,
                    containerOffset = container.offset().left,
                    containerWidth = container.outerWidth(),
                    minLeft = containerOffset + 10,
                    maxLeft = containerOffset + containerWidth - dragWidth - 10;
                
                dragElement.parents().on("mousemove vmousemove", function(e) {
                    if( !this.dragging) {
                        this.dragging =  true;
                        ( !window.requestAnimationFrame )
                            ? setTimeout(function(){this.animateDraggedHandle(e, xPosition, dragWidth, minLeft, maxLeft, containerOffset, containerWidth, resizeElement, labelContainer, labelResizeElement);}.bind(this), 100)
                            : requestAnimationFrame(function(){this.animateDraggedHandle(e, xPosition, dragWidth, minLeft, maxLeft, containerOffset, containerWidth, resizeElement, labelContainer, labelResizeElement);}.bind(this)); 
                    }
                }.bind(this)).on("mouseup vmouseup", function(e){
                    dragElement.removeClass('draggable');
                    resizeElement.removeClass('resizable');
                });
                e.preventDefault();
            }.bind(this)).on("mouseup vmouseup", function(e) {
                dragElement.removeClass('draggable');
                resizeElement.removeClass('resizable');
            });
        },

        animateDraggedHandle: function(e, xPosition, dragWidth, minLeft, maxLeft, containerOffset, containerWidth, resizeElement, labelContainer, labelResizeElement) {
            var leftValue = e.pageX + xPosition - dragWidth;   
            //constrain the draggable element to move inside his container
            if(leftValue < minLeft ) {
                leftValue = minLeft;
            } else if ( leftValue > maxLeft) {
                leftValue = maxLeft;
            }
    
            var widthValue = (leftValue + dragWidth/2 - containerOffset)*100/containerWidth+'%';
            
            $('.draggable').css('left', widthValue).on("mouseup vmouseup", function() {
                $(this).removeClass('draggable');
                resizeElement.removeClass('resizable');
            });
    
            $('.resizable').css('width', widthValue); 
    
            this.updateLabel(labelResizeElement, resizeElement, 'left');
            this.updateLabel(labelContainer, resizeElement, 'right');
            this.dragging =  false;
        },

        updateLabel: function(label, resizeElement, position) {
            if(position == 'left') {
                ( label.offset().left + label.outerWidth() < resizeElement.offset().left + resizeElement.outerWidth() ) ? label.removeClass('is-hidden') : label.addClass('is-hidden') ;
            } else {
                ( label.offset().left > resizeElement.offset().left + resizeElement.outerWidth() ) ? label.removeClass('is-hidden') : label.addClass('is-hidden') ;
            }
        }

    };

    return ImageCompare;
});