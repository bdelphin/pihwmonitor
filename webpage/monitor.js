const header = document.querySelector('header');
const section = document.querySelector('section');
const error = document.getElementById('error');

var cpu_article = document.getElementById("cpu_article");
var gpu_article = document.getElementById("gpu_article");
var watercooling_article = document.getElementById("watercooling_article");
var other_article = document.getElementById("other_article");

var cpu_raw = document.getElementById("cpu_raw");
var gpu_raw = document.getElementById("gpu_raw");
var watercooling_raw = document.getElementById("watercooling_raw");
var other_raw = document.getElementById("other_raw");

var cpu_header_1 = document.getElementById('cpu_header_1');
var cpu_header_2 = document.getElementById('cpu_header_2');            
var cpu_header_3 = document.getElementById('cpu_header_3');
var gpu_header_1 = document.getElementById('gpu_header_1');            
var gpu_header_2 = document.getElementById('gpu_header_2');
var gpu_header_3 = document.getElementById('gpu_header_3');            
var watercooling_header_1 = document.getElementById('watercooling_header_1');
var watercooling_header_2 = document.getElementById('watercooling_header_2');            
var watercooling_header_3 = document.getElementById('watercooling_header_3');
var other_header_1 = document.getElementById('other_header_1');            
var other_header_2 = document.getElementById('other_header_2');
var other_header_3 = document.getElementById('other_header_3');            

var cpu_canvas_1 = document.getElementById('cpu_canvas_1');
var cpu_canvas_2 = document.getElementById('cpu_canvas_2');            
var cpu_canvas_3 = document.getElementById('cpu_canvas_3');
var gpu_canvas_1 = document.getElementById('gpu_canvas_1');            
var gpu_canvas_2 = document.getElementById('gpu_canvas_2');
var gpu_canvas_3 = document.getElementById('gpu_canvas_3');            
var watercooling_canvas_1 = document.getElementById('watercooling_canvas_1');
var watercooling_canvas_2 = document.getElementById('watercooling_canvas_2');            
var watercooling_canvas_3 = document.getElementById('watercooling_canvas_3');
var other_canvas_1 = document.getElementById('other_canvas_1');            
var other_canvas_2 = document.getElementById('other_canvas_2');
var other_canvas_3 = document.getElementById('other_canvas_3');            

var cpu_value_1 = document.getElementById('cpu_value_1');
var cpu_value_2 = document.getElementById('cpu_value_2');            
var cpu_value_3 = document.getElementById('cpu_value_3');
var gpu_value_1 = document.getElementById('gpu_value_1');            
var gpu_value_2 = document.getElementById('gpu_value_2');
var gpu_value_3 = document.getElementById('gpu_value_3');            
var watercooling_value_1 = document.getElementById('watercooling_value_1');
var watercooling_value_2 = document.getElementById('watercooling_value_2');            
var watercooling_value_3 = document.getElementById('watercooling_value_3');
var other_value_1 = document.getElementById('other_value_1');            
var other_value_2 = document.getElementById('other_value_2');
var other_value_3 = document.getElementById('other_value_3');


var gauge_default_options = 
{
  angle: -0.15, // The span of the gauge arc
  lineWidth: 0.25, // The line thickness
  radiusScale: 1, // Relative radius
  pointer: {
    length: 0.57, // Relative to gauge radius
    strokeWidth: 0.042, // The thickness
    color: '#000000' // Fill color
  },
  limitMax: false,     // If false, max value increases automatically if value > maxValue
  limitMin: false,     // If true, the min value of the gauge will be fixed
  //colorStart: '#6FADCF',   // Colors
  //colorStop: '#8FC0DA',    // just experiment with them
  percentColors: [[0.0, "#a9ff0b" ], [0.75, "#f9c802"], [1.0, "#ff0000"]],
  strokeColor: '#E0E0E0',  // to see which ones work best for you
  generateGradient: true,
  highDpiSupport: true,     // High resolution support
}; 

var cpu_gauge_1 = createGauge(cpu_canvas_1, gauge_default_options, 100, 0, 32, 100);
var cpu_gauge_2 = createGauge(cpu_canvas_2, gauge_default_options, 100, 20, 32, 100);
var cpu_gauge_3 = createGauge(cpu_canvas_3, gauge_default_options, 4.5, 2.2, 32, 4.5);

var gpu_gauge_1 = createGauge(gpu_canvas_1, gauge_default_options, 110, 20, 32, 110);
var gpu_gauge_2 = createGauge(gpu_canvas_2, gauge_default_options, 100, 0, 32, 100);
var gpu_gauge_3 = createGauge(gpu_canvas_3, gauge_default_options, 3000, 0, 32, 3000);

var watercooling_gauge_1 = createGauge(watercooling_canvas_1, gauge_default_options, 60, 20, 32, 60); 
var watercooling_gauge_2 = createGauge(watercooling_canvas_2, gauge_default_options, 3000, 0, 32, 3000); 
var watercooling_gauge_3 = createGauge(watercooling_canvas_3, gauge_default_options, 3000, 0, 32, 3000); 

var other_gauge_1 = createGauge(other_canvas_1, gauge_default_options, 100, 0, 32, 100);
var other_gauge_2 = createGauge(other_canvas_2, gauge_default_options, 100, 0, 32, 100);
var other_gauge_3 = createGauge(other_canvas_3, gauge_default_options, 10, 0, 32, 10);

//getData();
setInterval(function(){ getData(); }, 1000);        

function getData()
{
    var requestURL = 'http://192.168.42.1:5000';
    var request = new XMLHttpRequest();
    request.open('GET', requestURL);
    request.onerror = function() { error.style.display = "block"; };
    request.responseType = 'json';
    request.send();
    request.onload = function() 
    {
        var json = request.response;
        
        // clear raw data section 
        cpu_raw.textContent = '';
        gpu_raw.textContent = '';
        watercooling_raw.textContent = '';
        other_raw.textContent = '';
        
        // hide error screen
        error.style.display = "none";
        
        // parse and display JSON data
        populateHeader(json);
        showData(json);
    }
}

function createGauge(canvas, options, maxValue, minValue, animationSpeed, defaultValue)
{
    var gauge = new Gauge(canvas).setOptions(options);
    gauge.maxValue = maxValue;
    gauge.setMinValue(minValue);
    gauge.animationSpeed = animationSpeed;
    gauge.set(defaultValue)
    
    return gauge;
}

function populateHeader(jsonObj) 
{
    var myH1 = document.getElementById("hostname");
    var myP = document.getElementById("system");
    myH1.textContent = jsonObj['hostname'];
    myP.textContent = jsonObj['system'];
}

function showData(jsonObj)
{
    var components = jsonObj['components'];
    components.forEach(component => 
    {
        if(component.label.includes('CPU'))
        {
            var currentArticle = cpu_article;
        }
        else if(component.label.includes('GPU'))
        {
            var currentArticle = gpu_article;
        }
        else if(component.label.includes('Watercooling'))
        {
            var currentArticle = watercooling_article;
        }
        else if(component.label.includes('Others'))
        {
            var currentArticle = other_article;
        }
        else
        {
            // no component should be here for now
        }

        // first child (h2) selection
        var label = currentArticle.firstElementChild;
        label.textContent = component.label;

        for (var i = 0; i < component['probe'].length; i++)
        {

            if(component['probe'][i].name.includes('Load'))
            {
                cpu_gauge_1.set(component['probe'][i].current);
                cpu_header_1.textContent = component['probe'][i].name;
                cpu_value_1.textContent = component['probe'][i].current + ' %';
                continue;
            }
            else if(component['probe'][i].name.includes('Tctl'))
            {
                cpu_gauge_2.set(component['probe'][i].current);
                cpu_header_2.textContent = component['probe'][i].name;
                cpu_value_2.textContent = component['probe'][i].current + ' °C';
                continue;
            }
            else if(component['probe'][i].name.includes('Freq'))
            {
                cpu_gauge_3.set(component['probe'][i].current);
                cpu_header_3.textContent = component['probe'][i].name;
                cpu_value_3.textContent = component['probe'][i].current + ' Ghz';
                continue;
            }                                    
            else if(component['probe'][i].name.includes('edge'))
            {
                gpu_gauge_1.set(component['probe'][i].current);
                gpu_header_1.textContent = component['probe'][i].name;
                gpu_value_1.textContent = component['probe'][i].current + ' °C';
                continue;
            }                           
            else if(component['probe'][i].name.includes('gpu load'))
            {
                gpu_gauge_2.set(component['probe'][i].current);
                // gpu_header_2.textContent = component['probe'][i].name;
                gpu_header_2.textContent = "Load";
                gpu_value_2.textContent = component['probe'][i].current + ' %';
                continue;
            }                           
            else if(component['probe'][i].name.includes('fan'))
            {
                gpu_gauge_3.set(component['probe'][i].current);
                // gpu_header_3.textContent = component['probe'][i].name;
                gpu_header_3.textContent = "Fan";
                gpu_value_3.textContent = component['probe'][i].current + ' RPM';
                continue;
            }                           
            else if(component['probe'][i].name.includes('Liquid'))
            {
                watercooling_gauge_1.set(component['probe'][i].current);
                watercooling_header_1.textContent = component['probe'][i].name;
                watercooling_value_1.textContent = component['probe'][i].current + ' °C';
                continue;
            }                           
            else if(component['probe'][i].name.includes('Fan 1'))
            {
                watercooling_gauge_2.set(component['probe'][i].current);
                watercooling_header_2.textContent = component['probe'][i].name;
                watercooling_value_2.textContent = component['probe'][i].current + ' RPM';
                continue;
            }
            else if(component['probe'][i].name.includes('Pump'))
            {
                watercooling_gauge_3.set(component['probe'][i].current);
                //watercooling_header_3.textContent = component['probe'][i].name;
                watercooling_header_3.textContent = "Pump";
                watercooling_value_3.textContent = component['probe'][i].current + ' RPM';
                continue;
            }
            else if(component['probe'][i].name.includes('RAM Usage'))
            {
                other_gauge_1.set(component['probe'][i].current);
                //other_header_1.textContent = component['probe'][i].name;
                other_header_1.textContent = "RAM";
                other_value_1.textContent = component['probe'][i].current + ' %';
                continue;
            }                           
            else if(component['probe'][i].name.includes('Disk'))
            {
                other_gauge_2.set(component['probe'][i].current);
                // other_header_2.textContent = component['probe'][i].name;
                other_header_2.textContent = "SSD";
                other_value_2.textContent = component['probe'][i].current + ' %';
                continue;
            }

            var p = document.createElement('span');
            if(component['probe'][i].type === 'temp')
                p.textContent = component['probe'][i].name + ': ' + component['probe'][i].current + ' °C';
            else if(component['probe'][i].type === 'fan')
                p.textContent = component['probe'][i].name + ': ' + component['probe'][i].current + ' RPM';
            else if(component['probe'][i].type === 'percent')
                p.textContent = component['probe'][i].name + ': ' + component['probe'][i].current + ' %';
            else if(component['probe'][i].type === 'freq')
                p.textContent = component['probe'][i].name + ': ' + component['probe'][i].current + ' Ghz';
            else if(component['probe'][i].type === 'ram_usage')
                p.textContent = component['probe'][i].name + ': ' + component['probe'][i].current + ' Gb / ' + component['probe'][i].max + ' Gb'; 
            
            // select current article last element child (div raw)
            currentArticle.lastElementChild.appendChild(p);
        }

    });
}


