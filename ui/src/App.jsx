import { useState } from 'react';
import Map, { NavigationControl, ScaleControl } from 'react-map-gl/maplibre';

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json';

export default function App() {
  const [coordinates, setCoordinates] = useState(null);

  return (
    <main className="workspace">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true" />
          <div>
            <strong>Interferometry</strong>
            <span>Earth observation workspace</span>
          </div>
        </div>
        <div className="status">
          <span className="status-dot" aria-hidden="true" />
          Map online
        </div>
      </header>

      <section className="map-shell" aria-label="Interactive map">
        <Map
          initialViewState={{ longitude: 0, latitude: 20, zoom: 2.2 }}
          mapStyle={MAP_STYLE}
          onMouseMove={({ lngLat }) => setCoordinates(lngLat)}
          attributionControl
        >
          <NavigationControl position="top-right" showCompass={false} />
          <ScaleControl position="bottom-right" unit="metric" />
        </Map>

        <aside className="map-panel">
          <p className="eyebrow">Active view</p>
          <h1>Global overview</h1>
          <dl>
            <div>
              <dt>Dataset</dt>
              <dd>None selected</dd>
            </div>
            <div>
              <dt>Coordinates</dt>
              <dd>
                {coordinates
                  ? `${coordinates.lat.toFixed(4)}, ${coordinates.lng.toFixed(4)}`
                  : 'Move over the map'}
              </dd>
            </div>
          </dl>
        </aside>
      </section>
    </main>
  );
}