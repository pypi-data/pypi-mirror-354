#ifndef EXAMPLE_COMPILE_TEST_HPP
#define EXAMPLE_COMPILE_TEST_HPP

#include <string>

struct simple_cast_test {
   static constexpr const char* id = "simple_cast";
   static constexpr bool expect_error = false;
   static constexpr const char* description = "Cast a length to a base_dimension length";

   template<typename = void>
   static void run() {
      int a = 5;
      double b = a;
   }
};

struct invalid_cast_test {
   static constexpr const char* id = "invalid_cast";
   static constexpr bool expect_error = true;
   static constexpr const char* description = "Fail to cast from one dimension to another";

   template<typename = void>
   static void run() {
      std::string a = "Five";
      int b = a;
   }
};

#endif // EXAMPLE_COMPILE_TEST_HPP
