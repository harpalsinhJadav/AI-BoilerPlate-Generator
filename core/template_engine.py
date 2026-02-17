"""
Template Generation Engine (Runnable V1)
----------------------------------------
Generates a fully runnable React Native project structure.
"""

from typing import Dict, List


# --------------------------------------------------
# Root runtime files
# --------------------------------------------------

def _app_js() -> str:
    return """import React from 'react';
import { Provider } from 'react-redux';
import AppNavigator from './src/navigation/AppNavigator';
import { store } from './src/store';

export default function App() {
  return (
    <Provider store={store}>
      <AppNavigator />
    </Provider>
  );
}
"""


def _index_js() -> str:
    return """import { AppRegistry } from 'react-native';
import App from './App';
import { name as appName } from './app.json';

AppRegistry.registerComponent(appName, () => App);
"""


# --------------------------------------------------
# Screens
# --------------------------------------------------

def _screen_component(name: str) -> str:
    return f"""import React from 'react';
import {{ View, Text }} from 'react-native';

export default function {name}Screen() {{
  return (
    <View style={{{{ flex: 1, alignItems: 'center', justifyContent: 'center' }}}}>
      <Text>{name} Screen</Text>
    </View>
  );
}}
"""


# --------------------------------------------------
# Components
# --------------------------------------------------

def _app_button() -> str:
    return """import React from 'react';
import { TouchableOpacity, Text } from 'react-native';
import { colors } from '../theme';

export default function AppButton({ title, onPress }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={{
        padding: 12,
        backgroundColor: colors.primary,
        borderRadius: 8,
      }}
    >
      <Text style={{ color: '#fff', textAlign: 'center' }}>{title}</Text>
    </TouchableOpacity>
  );
}
"""


# --------------------------------------------------
# Theme
# --------------------------------------------------

def _theme_colors() -> str:
    return """export const colors = {
  primary: '#007AFF',
  background: '#FFFFFF',
  text: '#111111',
  border: '#E5E5E5',
};
"""


def _theme_index() -> str:
    return """export * from './colors';
"""


# --------------------------------------------------
# Redux
# --------------------------------------------------

def _redux_slice() -> str:
    return """import { createSlice } from '@reduxjs/toolkit';

const sampleSlice = createSlice({
  name: 'sample',
  initialState: { value: 0 },
  reducers: {
    increment: state => { state.value += 1; },
    decrement: state => { state.value -= 1; },
  },
});

export const { increment, decrement } = sampleSlice.actions;
export default sampleSlice.reducer;
"""


def _redux_store() -> str:
    return """import { configureStore } from '@reduxjs/toolkit';
import sampleReducer from './sampleSlice';

export const store = configureStore({
  reducer: {
    sample: sampleReducer,
  },
});
"""


# --------------------------------------------------
# API
# --------------------------------------------------

def _api_client() -> str:
    return """import axios from 'axios';

const api = axios.create({
  baseURL: 'https://example.com/api',
});

api.interceptors.response.use(
  res => res,
  err => Promise.reject(err)
);

export default api;
"""


# --------------------------------------------------
# Navigation
# --------------------------------------------------

def _navigator(screens: List[str]) -> str:
    imports = "\n".join(
        f"import {s}Screen from '../screens/{s}Screen';" for s in screens
    )

    routes = "\n".join(
        f"<Stack.Screen name='{s}' component={{{s}Screen}} />" for s in screens
    )

    return f"""import React from 'react';
import {{ NavigationContainer }} from '@react-navigation/native';
import {{ createStackNavigator }} from '@react-navigation/stack';

{imports}

const Stack = createStackNavigator();

export default function AppNavigator() {{
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {routes}
      </Stack.Navigator>
    </NavigationContainer>
  );
}}
"""


# --------------------------------------------------
# Jest
# --------------------------------------------------

def _jest_config() -> str:
    return """module.exports = {
  preset: 'react-native',
  setupFilesAfterEnv: ['./jest.setup.js'],
};
"""


def _jest_setup() -> str:
    return """import '@testing-library/jest-native/extend-expect';
"""


def _jest_test(name: str) -> str:
    return f"""import React from 'react';
import renderer from 'react-test-renderer';
import {name}Screen from '../../src/screens/{name}Screen';

test('renders {name} screen', () => {{
  const tree = renderer.create(<{name}Screen />).toJSON();
  expect(tree).toBeTruthy();
}});
"""


# --------------------------------------------------
# Main generator
# --------------------------------------------------

def generate_templates(config: Dict) -> Dict[str, str]:
    files: Dict[str, str] = {}

    screens: List[str] = config["screens"]
    features: List[str] = config["features"]

    # Root runtime
    files["App.js"] = _app_js()
    files["index.js"] = _index_js()

    # Screens + tests
    for s in screens:
        files[f"src/screens/{s}Screen.js"] = _screen_component(s)
        files[f"tests/screens/{s}Screen.test.js"] = _jest_test(s)

    # Components
    files["src/components/AppButton.js"] = _app_button()

    # Theme
    files["src/theme/colors.js"] = _theme_colors()
    files["src/theme/index.js"] = _theme_index()

    # Redux
    if "redux" in features:
        files["src/store/sampleSlice.js"] = _redux_slice()
        files["src/store/index.js"] = _redux_store()

    # API
    if "axios" in features:
        files["src/api/client.js"] = _api_client()

    # Navigation
    files["src/navigation/AppNavigator.js"] = _navigator(screens)

    # i18n
    if "i18n" in features:
        files["src/i18n/en.json"] = '{ "welcome": "Welcome" }'

    # Jest
    files["jest.config.js"] = _jest_config()
    files["jest.setup.js"] = _jest_setup()

    return files
