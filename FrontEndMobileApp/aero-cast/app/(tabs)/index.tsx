import { Image, StyleSheet, Platform, View,Text, TextInput} from 'react-native';




export default function HomeScreen() {
  return (

    <View className="flex-1 bg-white">
      <View className="pt-10 pl-8">
        <Text className="text-blue text-3xl font-bold">Aero-Cast</Text>
        </View>

        <View className="pt-4 pl-4 pr-4">
  
         <TextInput
         placeholder='Search District'
         placeholderTextColor='gray'
         style="bg-gray-200 rounded-lg p-4 w-3/4"
         />

        </View>

        <View className="flex-1 pt-5 pl-4">
          <View className="w-3/4 p-5 bg-gray-700 rounded-lg">
          <Text className="text-white text-xl font-bold">Lilongwe</Text>

          </View>

          <View className="flex-row justify-between mt-3">
            <View className="bg-gray-600 rounded-lg p-3">
              <Text className="text-white">Temp</Text>
              <Text className="">34°C</Text>

            </View>

            <View className="bg-gray-600 rounded-lg p-3">
              <Text className="text-white">Humidity</Text>
              <Text className="">34°C</Text>

            </View>

            <View className="bg-gray-600 rounded-lg p-3">
              <Text className="text-white">Temp</Text>
              <Text className="">34°C</Text>

            </View>

            <View className="bg-gray-600 rounded-lg p-3">
              <Text className="text-white">Temp</Text>
              <Text className="">34°C</Text>

            </View>

          </View>


        </View>



      
    
    </View>
  
    
  );
}

