// NDWI and MNDWI calculation using Landsat 9 TOA
// Study Area: Ramganga Basin (RGB)

// Load Landsat 9 TOA
var imgCollection = ee.ImageCollection("LANDSAT/LC09/C02/T1_TOA")
  .filterBounds(Ramganga.geometry())
  .filterDate('2022-01-01', '2023-01-01')
  .filter(ee.Filter.lt('CLOUD_COVER', 30));

// Median image
var img = imgCollection.median();
var geometry = Ramganga.geometry();

// NDWI
var ndwi = img.normalizedDifference(['B3', 'B5']).rename('NDWI');
var ndwiClipped = ndwi.clip(geometry);

// MNDWI
var mndwi = img.normalizedDifference(['B3', 'B6']).rename('MNDWI');
var mndwiClipped = mndwi.clip(geometry);

// Visualization
Map.centerObject(geometry, 10);
Map.addLayer(ndwiClipped, {min: -1, max: 1, palette: ['white', 'blue']}, 'NDWI');
Map.addLayer(mndwiClipped, {min: -1, max: 1, palette: ['white', 'green']}, 'MNDWI');

// Export NDWI
Export.image.toDrive({
  image: ndwiClipped,
  description: 'NDWI_Ramganga',
  scale: 30,
  region: geometry,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});

// Export MNDWI
Export.image.toDrive({
  image: mndwiClipped,
  description: 'MNDWI_Ramganga',
  scale: 30,
  region: geometry,
  fileFormat: 'GeoTIFF',
  maxPixels: 1e13
});
