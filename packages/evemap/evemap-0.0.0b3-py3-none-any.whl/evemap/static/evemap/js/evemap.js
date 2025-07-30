(function() {
// right at the top
var eveProjection = new ol.proj.Projection({
	code: 'EVE:SYS',
	units: 'm',
	extent: [-250000000000000000, -250000000000000000, 250000000000000000, 250000000000000000],
	global: false,
	metersPerUnit: 1
});
ol.proj.addProjection(eveProjection);

// point colour
function getColorForValue(value) {

	if (value > 0.9) {
		return '#2e74dc';
	} else if (value > 0.8) {
		return '#389cf3';
	} else if (value > 0.7) {
		return '#4acff2';
	} else if (value > 0.6) {
		return '#60daa6';
	} else if (value > 0.5) {
		return '#71e452';
	} else if (value > 0.4) {
		return '#eeff83';
	} else if (value > 0.3) {
		return '#e16a0b';
	} else if (value > 0.2) {
		return '#d1440d';
	} else if (value > 0.1) {
		return '#bc1114';
	} else if (value > 0.0) {
		return '#6d2122';
	} else {
		return '#8f2f69';
	}
  }

  const pointStyleFunction = function(feature, resolution) {
	const attr = feature.get('security_status');
	const fillColor = getColorForValue(attr);
	const zoom = map.getView().getZoom();
	const radius = 0 + (zoom * 1);

	return new ol.style.Style({
	  image: new ol.style.Circle({
		radius: radius,
		fill: new ol.style.Fill({ color: fillColor }),
	  }),
	});
  };

  const constellationStyleFunction = function(feature) {
	return new ol.style.Style({
	  stroke: new ol.style.Stroke({
		color: 'yellow',
		width: 1
	  }),
	  fill: new ol.style.Fill({
		color: 'rgba(0, 255, 255, 0.1)'
	  }),
	  text: new ol.style.Text({
		text: feature.get('constellation_name') || '', // Get the 'name' attribute
		font: '13px Calibri,sans-serif',
		fill: new ol.style.Fill({ color: '#fff' }),
		stroke: new ol.style.Stroke({ color: '#000', width: 1 }),
		overflow: true
	  })
	});
  };

  const regionStyleFunction = function(feature) {
	return new ol.style.Style({
	  stroke: new ol.style.Stroke({
		color: 'blue',
		width: 1
	  }),
	  fill: new ol.style.Fill({
		color: 'rgba(0, 0, 255, 0.1)'
	  }),
	  text: new ol.style.Text({
		text: feature.get('region_name') || '', // Get the 'name' attribute
		font: '13px Calibri,sans-serif',
		fill: new ol.style.Fill({ color: '#fff' }),
		stroke: new ol.style.Stroke({ color: '#000', width: 1 }),
		overflow: true
	  })
	});
  };

  const lineStyle = new ol.style.Style({
	stroke: new ol.style.Stroke({
	  color: 'rgba(255, 255, 255, 0.1)',
	  width: 1,
	  lineDash: [10, 10],
	  lineCap: 'round',
	  lineJoin: 'round',
	}),
  });

var solarSystemsLayer = new ol.layer.Vector({
	title: 'Solar Systems',
	source: new ol.source.Vector({
		url: url_solar_systems_points,
		format: new ol.format.GeoJSON()
	}),
	style: pointStyleFunction
});

var constellationsLayer = new ol.layer.Vector({
	title: 'Constellations',
	source: new ol.source.Vector({
		url: url_constellations_polygons,
		format: new ol.format.GeoJSON()
	}),
	style: regionStyleFunction
});

var regionsLayer = new ol.layer.Vector({
	title: 'Regions',
	source: new ol.source.Vector({
		url: url_regions_polygons,
		format: new ol.format.GeoJSON()
	}),
	style: regionStyleFunction
});

var gatesLayer = new ol.layer.Vector({
	title: 'Gate Network',
	source: new ol.source.Vector({
		url: url_stargates_lines,
		format: new ol.format.GeoJSON()
	}),
	style: lineStyle
});

var overlayGroup = new ol.layer.Group({
	title: 'Overlays',
	layers: [regionsLayer, constellationsLayer, solarSystemsLayer, gatesLayer]
  });

var map = new ol.Map({
	target: 'map',
	layers: [overlayGroup],
	view: new ol.View({
		projection: eveProjection,
		center: [0, 0],
		zoom: 1
	})
});

var layerSwitcher = new ol.control.LayerSwitcher({
	tipLabel: 'Layers', // Optional label for the button
	activationMode: 'click', // or 'mouseover'
	startActive: true, // Panel starts closed
	groupSelectStyle: 'children' // Controls group selection behavior
  });
  map.addControl(layerSwitcher);

var popup = document.getElementById('popup');
map.on('singleclick', function(evt) {
	var feature = map.forEachFeatureAtPixel(evt.pixel, function(feat) {
		return feat;
	});
	if (feature) {
		popup.innerHTML = "";
		var props = feature.getProperties();
		delete props.geometry;
		if (props.region_name !== undefined) {
			popup.innerHTML += 'Region: ' + props.region_name + '<br />';
		}
		if (props.name !== undefined) {
			popup.innerHTML += 'System: ' + props.name + '<br />';
		}
		if (props.security_status !== undefined) {
			popup.innerHTML += 'Security Status: ' + props.security_status.toFixed(3) + '<br />';
		}
		popup.style.display = 'block';
		var coordinate = evt.coordinate;
		var pixel = map.getPixelFromCoordinate(coordinate);
		popup.style.left = (pixel[0]) + 'px';
		popup.style.top = (pixel[1]) + 'px';
	} else {
		popup.style.display = 'none';
	}
});

})();
