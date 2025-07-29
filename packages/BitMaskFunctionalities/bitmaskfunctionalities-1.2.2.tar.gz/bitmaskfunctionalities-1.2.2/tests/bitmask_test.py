import pytest

# Import the BitMask class and helper functions from your module
from BitMask import BitMask
from BitMask.bitmask_module import (_MAX_BITMASK_LENGTH,
                                    _value_validation,
                                    _index_validation,
                                    _sliceable_index_validation,
                                    _string_value_validation,
                                    _bit_mask_length_validation,
                                    _shift_validation)


# noinspection PyTypeChecker
class TestBitMask:
    # --- Test Helper Functions (Validation) ---

    def test_value_validation(self):
        # Test valid cases
        _value_validation(10, 16)
        _value_validation(0, 16)
        _value_validation(15, 16)

        # Test invalid cases
        with pytest.raises(TypeError):
            _value_validation("not_int", 16)
        with pytest.raises(ValueError):
            _value_validation(-1, 16)
        with pytest.raises(ValueError):
            _value_validation(16, 16)
        with pytest.raises(ValueError):
            _value_validation(100, 10)

    def test_index_validation(self):
        # Test valid cases
        _index_validation(0, 8)
        _index_validation(7, 8)
        _index_validation([0, 1, 7], 8)
        _index_validation((0, 1, 7), 8)
        _index_validation([], 8)  # Empty list/tuple

        # Test invalid cases
        with pytest.raises(IndexError):
            _index_validation(-1, 8)
        with pytest.raises(IndexError):
            _index_validation(8, 8)
        with pytest.raises(TypeError):
            _index_validation("not_int", 8)
        with pytest.raises(TypeError):
            _index_validation([0, "not_int"], 8)
        with pytest.raises(IndexError):
            _index_validation([0, 8], 8)
        with pytest.raises(IndexError):
            _index_validation((0, -1), 8)

    def test_sliceable_index_validation(self):
        # Test valid cases
        _sliceable_index_validation(0, 8)
        _sliceable_index_validation(7, 8)
        _sliceable_index_validation(slice(0, 8), 8)
        _sliceable_index_validation(slice(None, None, 2), 8)  # ::2
        _sliceable_index_validation(slice(7, 0, -1), 8)  # Reverse slice
        _sliceable_index_validation(-1, 8)

        # Test invalid cases
        with pytest.raises(IndexError):
            _sliceable_index_validation(8, 8)
        with pytest.raises(ValueError):
            _sliceable_index_validation(slice(0, 0), 8)  # Empty slice
        with pytest.raises(ValueError):
            _sliceable_index_validation(slice(5, 5), 8)  # Empty slice
        with pytest.raises(ValueError):
            # Out of range, leading to empty slice
            _sliceable_index_validation(slice(10, 12),
                                        8)
        with pytest.raises(TypeError):
            _sliceable_index_validation("not_int_or_slice", 8)

    def test_string_value_validation(self):
        # Test valid cases
        assert _string_value_validation("101", 2) == 5
        assert _string_value_validation("0b101", 2) == 5
        assert _string_value_validation("FF", 16) == 255
        assert _string_value_validation("0xff", 16) == 255
        assert _string_value_validation("123", 10) == 123

        # Test invalid cases
        with pytest.raises(ValueError):
            _string_value_validation("not_a_num", 2)
        with pytest.raises(TypeError):
            _string_value_validation(123, 10)  # not string
        with pytest.raises(ValueError):
            _string_value_validation("abc", 10)  # Invalid for base 10
        with pytest.raises(ValueError):
            _string_value_validation("FAF", 2)

    def test_bit_mask_length_validation(self):
        # Test valid case
        other_bitmask_valid = BitMask(8)
        _bit_mask_length_validation(other_bitmask_valid, 8, "op")

        # Test invalid cases
        other_bitmask_invalid_7 = BitMask(7)
        other_bitmask_invalid_9 = BitMask(9)
        with pytest.raises(TypeError):
            _bit_mask_length_validation(other_bitmask_invalid_7, 8, "op")
        with pytest.raises(TypeError):
            _bit_mask_length_validation(other_bitmask_invalid_9, 8, "op")

    def test_shift_validation(self):
        # Test valid cases
        _shift_validation(5, False)
        _shift_validation(5, True)
        _shift_validation(_MAX_BITMASK_LENGTH,
                          True)  # Edge case for max allowed left shift
        assert _shift_validation("not_int",
                                 False) is None  # Should return, not raise

        # Test invalid cases
        with pytest.raises(ValueError):
            _shift_validation(-1, False)
        with pytest.raises(ValueError):
            _shift_validation(-1, True)
        with pytest.raises(ValueError):
            _shift_validation(_MAX_BITMASK_LENGTH + 1,
                              True)  # Exceeds max left shift

    # --- Test BitMask Class Methods ---

    def test_initialization(self):
        # Test valid cases with validation enabled
        bm = BitMask(8, 0, enable_validation=True)
        assert bm.max_length == 8
        assert bm.value == 0

        bm = BitMask(1, 0, enable_validation=True)
        assert bm.max_length == 1
        assert bm.value == 0

        bm = BitMask(_MAX_BITMASK_LENGTH, (1 << (_MAX_BITMASK_LENGTH - 1)),
                     enable_validation=True)
        assert bm.max_length == _MAX_BITMASK_LENGTH
        assert bm.value == (1 << (_MAX_BITMASK_LENGTH - 1))

        # Test valid cases with validation disabled
        bm = BitMask(8, 0, enable_validation=False)
        assert bm.max_length == 8
        assert bm.value == 0

    def test_initialization_errors(self):
        # Test errors with validation enabled
        with pytest.raises(TypeError):
            BitMask("not_int", 0, enable_validation=True)
        with pytest.raises(ValueError):
            BitMask(0, 0, enable_validation=True)
        with pytest.raises(ValueError):
            BitMask(-5, 0, enable_validation=True)
        with pytest.raises(ValueError):
            BitMask(_MAX_BITMASK_LENGTH + 1, 0, enable_validation=True)
        with pytest.raises(TypeError):
            BitMask(8, "not_int", enable_validation=True)
        with pytest.raises(ValueError):
            BitMask(8, -1, enable_validation=True)
        with pytest.raises(ValueError):
            BitMask(8, 256,
                    enable_validation=True)  # value >= upper_bound (2^8)

    def test_initialization_disable_validation(self):
        # Test that init does NOT raise when validation is disabled
        # These would normally raise errors
        try:
            bm = BitMask(0, 0, enable_validation=False)
            assert bm.max_length == 0
            assert bm.value == 0
        except Exception as e:
            pytest.fail(
                f"BitMask.__init__ unexpectedly raised {type(e).__name__} "
                f"when validation disabled for length 0.")

        try:
            bm = BitMask(_MAX_BITMASK_LENGTH + 1, 0, enable_validation=False)
            assert bm.max_length == _MAX_BITMASK_LENGTH + 1
            assert bm.value == 0
        except Exception as e:
            pytest.fail(
                f"BitMask.__init__ unexpectedly raised {type(e).__name__} "
                f"when validation disabled for large length.")

        try:
            bm = BitMask(8, "not_int", enable_validation=False)
            assert bm.max_length == 8
            assert bm.value == "not_int"
        except Exception as e:
            pytest.fail(
                f"BitMask.__init__ unexpectedly raised {type(e).__name__} "
                f"when validation disabled for value type.")

        try:
            bm = BitMask(8, -1, enable_validation=False)
            assert bm.max_length == 8
            assert bm.value == -1
        except Exception as e:
            pytest.fail(
                f"BitMask.__init__ unexpectedly raised {type(e).__name__} "
                f"when validation disabled for negative value.")

    def test_properties(self):
        bm = BitMask(8)
        assert bm.max_length == 8
        assert bm.value == 0
        bm.value = 15
        assert bm.value == 15

    def test_value_setter_errors(self):
        bm = BitMask(8)
        with pytest.raises(TypeError):
            bm.value = "invalid"
        with pytest.raises(ValueError):
            bm.value = 256  # 1 << 8

    def test_set_bits(self):
        bm = BitMask(8)
        bm.set_bits(0)
        assert bm.value == 0b00000001
        bm.set_bits(3)
        assert bm.value == 0b00001001  # 9

        bm = BitMask(8)
        bm.set_bits([0, 2])
        assert bm.value == 0b00000101  # 5
        bm.set_bits((1, 3))
        assert bm.value == 0b00001111  # 15

        bm = BitMask(8, 0b11111111)
        bm.set_bits([])  # Empty list/tuple
        assert bm.value == 0b11111111

    def test_set_bits_errors(self):
        bm = BitMask(8)
        with pytest.raises(TypeError):
            bm.set_bits(1.5)
        with pytest.raises(IndexError):
            bm.set_bits(8)
        with pytest.raises(TypeError):
            bm.set_bits([0, "a"])

    def test_set_all(self):
        bm = BitMask(5)
        bm.set_all()
        assert bm.value == (1 << 5) - 1  # 31
        bm = BitMask(7)
        bm.set_all()
        assert bm.value == (1 << 7) - 1  # 127

    def test_flip_bits(self):
        bm = BitMask(8, 0b00101011)  # 43
        bm.flip_bits(0)
        assert bm.value == 0b00101010  # 42
        bm.flip_bits(1)
        assert bm.value == 0b00101000  # 40

        bm = BitMask(8, 0b00101011)
        bm.flip_bits([0, 2])
        assert bm.value == (0b00101011 ^ 0b00000101)  # 43 ^ 5 = 46 (00101110)
        bm.flip_bits((1, 3))
        assert bm.value == (
                0b00101110 ^ 0b00001010)  # 43 ^ 10 ^ 5 = 36 (00100100)

        bm = BitMask(8, 0b11111111)
        bm.flip_bits([])  # Empty list/tuple
        assert bm.value == 0b11111111

    def test_flip_bits_errors(self):
        bm = BitMask(8)
        with pytest.raises(TypeError):
            bm.flip_bits(1.5)
        with pytest.raises(IndexError):
            bm.flip_bits(8)
        with pytest.raises(TypeError):
            bm.flip_bits([0, "a"])

    def test_flip_all(self):
        bm = BitMask(8, 0b00101011)  # 43
        bm.flip_all()
        assert bm.value == (0b00101011 ^ 0b11111111)  # 212
        bm.flip_all()  # Flip back
        assert bm.value == 0b00101011  # 43

    def test_clear_bits(self):
        bm = BitMask(8, 0b11111111)  # 255
        bm.clear_bits(0)
        assert bm.value == 0b11111110  # 254
        bm.clear_bits(3)
        assert bm.value == 0b11110110  # 246

        bm = BitMask(8, 0b11111111)
        bm.clear_bits([0, 2])
        assert bm.value == (
                0b11111111 & ~0b00000101)  # 255 & ~5 = 250 (11111010)
        bm.clear_bits((1, 3))
        assert bm.value == (
                0b11111111 & ~0b00001111)  # 255 & ~10 & ~5 = 240 (11110000)

        bm = BitMask(8, 0b00000000)
        bm.clear_bits([])  # Empty list/tuple
        assert bm.value == 0b00000000

    def test_clear_bits_errors(self):
        bm = BitMask(8)
        with pytest.raises(TypeError):
            bm.clear_bits(1.5)
        with pytest.raises(IndexError):
            bm.clear_bits(8)
        with pytest.raises(TypeError):
            bm.clear_bits([0, "a"])

    def test_clear_all(self):
        bm = BitMask(8, 0b10101010)
        bm.clear_all()
        assert bm.value == 0
        bm = BitMask(5, 0b11111)
        bm.clear_all()
        assert bm.value == 0

    def test_reverse_bit_order(self):
        bm = BitMask(4, 0b0101)  # 5
        bm.reverse_bit_order()
        assert bm.value == 0b1010  # 10
        bm = BitMask(7, 0b0101011)  # 43
        bm.reverse_bit_order()
        assert bm.value == 0b1101010  # 106
        bm = BitMask(6, 0b010101)  # 21
        bm.reverse_bit_order()
        assert bm.value == 0b101010  # 42
        bm = BitMask(8, 0)
        bm.reverse_bit_order()
        assert bm.value == 0
        bm = BitMask(8, 255)
        bm.reverse_bit_order()
        assert bm.value == 255

    def test_get_bits(self):
        bm = BitMask(8, 0b10110110)  # 182
        assert bm.get_bits(0) == 0
        assert bm.get_bits(1) == 1
        assert bm.get_bits(7) == 1

        assert bm.get_bits([0, 1, 2, 3]) == (0, 1, 1, 0)
        assert bm.get_bits((7, 6, 5)) == (1, 0, 1)
        assert bm.get_bits([]) == ()

    def test_get_bits_errors(self):
        bm = BitMask(8)
        with pytest.raises(TypeError):
            bm.get_bits(1.5)
        with pytest.raises(IndexError):
            bm.get_bits(8)
        with pytest.raises(TypeError):
            bm.get_bits([0, "a"])

    def test_get_count(self):
        bm = BitMask(8, 0b10101010)  # 170
        assert bm.get_count() == 4
        bm = BitMask(6, 0b111111)  # 63
        assert bm.get_count() == 6
        bm = BitMask(4, 0)
        assert bm.get_count() == 0

    def test_get_set_bits(self):
        bm = BitMask(8, 0b01011010)  # 90
        assert bm.get_set_bits() == (1, 3, 4, 6)
        bm = BitMask(8, 0)
        assert bm.get_set_bits() == ()
        bm = BitMask(8, 255)
        assert bm.get_set_bits() == (0, 1, 2, 3, 4, 5, 6, 7)

    def test_get_cleared_bits(self):
        bm = BitMask(8, 0b01011010)  # 90
        assert bm.get_cleared_bits() == (0, 2, 5, 7)
        bm = BitMask(8, 255)
        assert bm.get_cleared_bits() == ()
        bm = BitMask(8, 0)
        assert bm.get_cleared_bits() == (0, 1, 2, 3, 4, 5, 6, 7)

    def test_get_lsb(self):
        bm = BitMask(8, 0b00101000)  # 40
        assert bm.get_lsb() == 3
        bm = BitMask(5, 0b00001)  # 1
        assert bm.get_lsb() == 0
        bm = BitMask(3, 0)
        assert bm.get_lsb() == -1

    def test_get_msb(self):
        bm = BitMask(8, 0b00101000)  # 40
        assert bm.get_msb() == 5  # 0b00101000 -> MSB is at index 5
        bm = BitMask(5, 0b00001)  # 1
        assert bm.get_msb() == 0
        bm = BitMask(3, 0)
        assert bm.get_msb() == -1

    def test_set_binary(self):
        bm = BitMask(8)
        bm.set_binary("101101")
        assert bm.value == 0b00101101  # 45
        bm.set_binary("0B00011")
        assert bm.value == 0b00000011  # 3

    def test_set_binary_errors(self):
        bm = BitMask(8)
        with pytest.raises(TypeError):
            bm.set_binary(101)
        with pytest.raises(TypeError):
            bm.set_binary([0b00011])
        with pytest.raises(ValueError):
            bm.set_binary("0B1201")  # Invalid binary digit
        with pytest.raises(ValueError):
            bm.set_binary("111111111")  # Too long for 8-bit mask
        with pytest.raises(ValueError):
            bm.set_binary("-0b10")  # Negative value
        with pytest.raises(ValueError):
            bm.set_binary("0x10")  # Wrong base format

    def test_set_hexadecimal(self):
        bm = BitMask(8)
        bm.set_hexadecimal("A5")
        assert bm.value == 0xA5  # 165
        bm.set_hexadecimal("0xF")
        assert bm.value == 0xF  # 15
        bm = BitMask(7)
        bm.set_hexadecimal("0X54")
        assert bm.value == 0x54  # 84

    def test_set_hexadecimal_errors(self):
        bm = BitMask(8)
        with pytest.raises(TypeError):
            bm.set_hexadecimal(0xA)
        with pytest.raises(TypeError):
            bm.set_hexadecimal(1.3)
        with pytest.raises(ValueError):
            bm.set_hexadecimal("G")  # Invalid hex digit
        with pytest.raises(ValueError):
            bm.set_hexadecimal("1000")  # Too large for 8-bit mask
        with pytest.raises(ValueError):
            bm.set_hexadecimal("-1")  # Negative value
        with pytest.raises(ValueError):
            bm.set_hexadecimal("0b0110")  # Wrong base format
        with pytest.raises(ValueError):
            bm.set_hexadecimal("0x1FF")  # Too large for 8-bit mask

    def test_set_decimal(self):
        bm = BitMask(8)
        bm.set_decimal("42")
        assert bm.value == 42
        bm = BitMask(4)
        bm.set_decimal("7")
        assert bm.value == 7

    def test_set_decimal_errors(self):
        bm = BitMask(8)
        with pytest.raises(TypeError):
            bm.set_decimal(5)  # Not a string
        with pytest.raises(ValueError):
            bm.set_decimal("0b0010")  # Wrong base format
        with pytest.raises(ValueError):
            bm.set_decimal("-1")  # Negative value
        with pytest.raises(ValueError):
            bm.set_decimal("256")  # Too large for 8-bit mask

    def test_to_binary(self):
        bm = BitMask(6, 0b101101)  # 45
        assert bm.to_binary() == "0b101101"
        bm = BitMask(4, 0b0101)  # 5
        assert bm.to_binary() == "0b0101"
        bm = BitMask(8, 0b00000000)
        assert bm.to_binary() == "0b00000000"
        bm = BitMask(8, 0b11111111)
        assert bm.to_binary() == "0b11111111"

    def test_to_hexadecimal(self):
        bm = BitMask(8, 0xAA)  # 170
        assert bm.to_hexadecimal() == "0xaa"
        bm = BitMask(6, 0xF)  # 15
        assert bm.to_hexadecimal() == "0x0f"
        bm = BitMask(4, 0)
        assert bm.to_hexadecimal() == "0x0"
        bm = BitMask(1, 1)
        assert bm.to_hexadecimal() == "0x1"
        bm = BitMask(5, 0b11010)  # 26
        assert bm.to_hexadecimal() == "0x1a"

    def test_to_decimal(self):
        bm = BitMask(5, 27)
        assert bm.to_decimal() == "27"
        bm = BitMask(30, 27)
        assert bm.to_decimal() == "27"
        bm = BitMask(1, 0)
        assert bm.to_decimal() == "0"
        bm = BitMask(1, 1)
        assert bm.to_decimal() == "1"

    def test_str(self):
        bm = BitMask(4, 0b0101)  # 5
        assert str(bm) == "0 1 0 1"
        bm = BitMask(7, 0b0101001)  # 41
        assert str(bm) == "0 1 0 1 0 0 1"
        bm = BitMask(3, 0)
        assert str(bm) == "0 0 0"
        bm = BitMask(3, 0b111)
        assert str(bm) == "1 1 1"

    def test_repr(self):
        bm = BitMask(8, 123)
        assert repr(bm) == "BitMask(8, 123, enable_validation=True)"
        bm = BitMask(1, 0, enable_validation=False)
        assert repr(bm) == "BitMask(1, 0, enable_validation=False)"

    def test_getitem_index(self):
        bm = BitMask(5, 0b01101)  # 13
        assert bm[0] == 1
        assert bm[1] == 0
        assert bm[4] == 0
        assert bm[-1] == 0  # Last bit (MSB)
        assert bm[-5] == 1  # First bit (LSB)

    def test_getitem_index_errors(self):
        bm = BitMask(3)
        with pytest.raises(IndexError):
            _ = bm[3]
        with pytest.raises(IndexError):
            _ = bm[-4]
        with pytest.raises(TypeError):
            _ = bm[1.5]
        with pytest.raises(TypeError):
            _ = bm["0b01"]

    def test_getitem_slice(self):
        bm = BitMask(8, 0b10101010)  # 170
        assert bm[0:3].value == 0b010  # 2 (bits 0,1,2)
        assert bm[2:6].value == 0b1010  # 10 (bits 2,3,4,5)
        assert bm[:4].value == 0b1010  # 10 (bits 0,1,2,3)
        assert bm[4:].value == 0b1010  # 10 (bits 4,5,6,7)
        assert bm[::-1].value == 0b01010101  # 85 (full reverse)
        assert bm[
               6::-1].value == 0b0101010  # 42 (reverse from index 6 down to 0)
        assert bm[
               6:2:-1].value == 0b1010  # 10 (reverse from index 6 down to 3)

    def test_setitem_index(self):
        bm = BitMask(6)
        bm[0] = 1
        assert bm.value == 0b000001
        bm[3] = 1
        assert bm.value == 0b001001  # 9
        bm[0] = 0
        assert bm.value == 0b001000  # 8
        bm[-1] = 1  # Set MSB
        assert bm.value == 0b101000  # 40

    def test_setitem_index_errors(self):
        bm = BitMask(3)
        with pytest.raises(TypeError):
            bm[1.5] = 1
        with pytest.raises(TypeError):
            bm["2"] = 1
        with pytest.raises(IndexError):
            bm[3] = 1
        with pytest.raises(IndexError):
            bm[-4] = 1
        with pytest.raises(ValueError):
            bm[1] = 2  # Value not 0 or 1

    def test_setitem_slice(self):
        bm = BitMask(8)  # 00000000
        bm[0:4] = 0b1010  # Set lower 4 bits to 1010 (0101 in LSB-first)
        assert bm.value == 0b00001010  # 10

        bm = BitMask(8)
        bm[4:8] = 0b0101  # Set upper 4 bits to 0101 (1010 in LSB-first)
        assert bm.value == 0b01010000  # 80

        bm = BitMask(8)
        bm[1:4] = 0b101  # Set bits 1,2,3 with 101 (0-indexed LSB of 101)
        assert bm.value == 0b00001010  # 10

        bm = BitMask(8, 0b11111111)
        bm[0:8:2] = 0b1010  # Set even bits (0,2,4,6) to 1010
        assert bm.value == 0b11101110  # 238

    def test_setitem_runtimewarning(self):
        bm = BitMask(8)
        with pytest.warns(RuntimeWarning,
                          match="Value .* has more bits .* than slice .*"):
            bm[0:4] = 0b10000  # Value 16 (5 bits) into a 4-bit slice

    def test_len(self):
        bm = BitMask(12)
        assert len(bm) == 12
        bm = BitMask(5)
        assert len(bm) == 5

    def test_equality(self):
        bm1 = BitMask(5, 7)
        bm2 = BitMask(5, 7)
        bm3 = BitMask(5, 10)
        bm4 = BitMask(6, 7)
        assert bm1 == bm2
        assert bm1 != bm3
        assert bm3 != 7
        assert bm4 == 7
        assert bm1.__ne__(bm4)
        assert bm1.__eq__("7") is NotImplemented

    def test_inequality(self):
        bm1 = BitMask(4, 3)
        bm2 = BitMask(4, 5)
        bm3 = BitMask(5, 5)  # Different length
        assert bm1 < bm2
        assert bm1 <= bm2
        assert bm2 > bm1
        assert bm2 >= bm1
        assert bm1 < 5
        assert bm1 <= 3
        assert bm2 > 2
        assert bm2 >= 5
        with pytest.raises(TypeError):
            _ = bm1 < bm3
        with pytest.raises(TypeError):
            _ = bm3 >= bm2

    def test_iteration(self):
        bm = BitMask(5, 0b01101)  # 13
        bits = [bit for bit in bm]
        assert bits == [1, 0, 1, 1, 0]  # LSB to MSB
        bm = BitMask(6, 0b001000)  # 8
        bits = [bit for bit in bm]
        assert bits == [0, 0, 0, 1, 0, 0]

    def test_invert(self):
        bm = BitMask(4, 0b1001)  # 9
        assert (~bm).value == 0b0110  # 6
        bm = BitMask(6, 0b010000)  # 16
        assert (~bm).value == 0b101111  # 47

    def test_hash(self):
        bm = BitMask(3, 5)
        with pytest.raises(TypeError):
            hash(bm)  # BitMask objects are unhashable

    def test_bitwise_and(self):
        bm1 = BitMask(4, 0b0110)  # 6
        bm2 = BitMask(4, 0b1101)  # 13
        result_bm = bm1 & bm2
        assert isinstance(result_bm, BitMask)
        assert result_bm.max_length == 4
        assert result_bm.value == (0b0110 & 0b1101)  # 0b0100 (4)

        result_int = bm1 & 0b0010  # 2
        assert isinstance(result_int, BitMask)
        assert result_int.value == (0b0110 & 0b0010)  # 0b0010 (2)

    def test_bitwise_or(self):
        bm1 = BitMask(4, 0b0110)  # 6
        bm2 = BitMask(4, 0b1010)  # 10
        result_bm = bm1 | bm2
        assert isinstance(result_bm, BitMask)
        assert result_bm.max_length == 4
        assert result_bm.value == (0b0110 | 0b1010)  # 0b1110 (14)

        result_int = bm1 | 0b0001  # 1
        assert isinstance(result_int, BitMask)
        assert result_int.value == (0b0110 | 0b0001)  # 0b0111 (7)

    def test_bitwise_xor(self):
        bm1 = BitMask(4, 0b0110)  # 6
        bm2 = BitMask(4, 0b1101)  # 13
        result_bm = bm1 ^ bm2
        assert isinstance(result_bm, BitMask)
        assert result_bm.max_length == 4
        assert result_bm.value == (0b0110 ^ 0b1101)  # 0b1011 (11)

        result_int = bm1 ^ 0b0010  # 2
        assert isinstance(result_int, BitMask)
        assert result_int.value == (0b0110 ^ 0b0010)  # 0b0100 (4)

    def test_bitwise_ops_errors(self):
        bm = BitMask(8)
        with pytest.raises(ValueError):
            bm & 256  # Integer value out of bounds
        with pytest.raises(TypeError):
            bm | BitMask(7)  # Different lengths
        with pytest.raises(TypeError):
            bm ^= "string"

    def test_lshift(self):
        bm = BitMask(4, 0b0001)  # 1
        result_bm = bm << 1
        assert isinstance(result_bm, BitMask)
        assert result_bm.max_length == 4
        assert result_bm.value == 0b0010  # 2

        bm = BitMask(4, 0b1000)  # 8
        result_bm = bm << 1  # Shift out of bounds (for 4-bit)
        assert result_bm.value == 0b0000  # 0

    def test_rshift(self):
        bm = BitMask(4, 0b1000)  # 8
        result_bm = bm >> 1
        assert isinstance(result_bm, BitMask)
        assert result_bm.max_length == 4
        assert result_bm.value == 0b0100  # 4

        bm = BitMask(4, 0b0001)  # 1
        result_bm = bm >> 1
        assert result_bm.value == 0b0000  # 0

    def test_shift_ops_errors(self):
        bm = BitMask(8)
        with pytest.raises(ValueError):
            bm << -1  # Negative shift count
        with pytest.raises(ValueError):
            bm >> -1  # Negative shift count
        with pytest.raises(ValueError):
            bm << (_MAX_BITMASK_LENGTH + 1)  # Excessive left shift
        with pytest.raises(TypeError):
            bm ^= "string"

    def test_iand(self):
        bm = BitMask(4, 0b0110)  # 6
        original_id = id(bm)
        bm &= 0b0010  # 2
        assert id(bm) == original_id
        assert bm.value == 0b0010  # 2

        bm = BitMask(4, 0b0110)
        bm2 = BitMask(4, 0b1101)  # 13
        original_id = id(bm)
        bm &= bm2
        assert id(bm) == original_id
        assert bm.value == 0b0100  # 4

    def test_ior(self):
        bm = BitMask(4, 0b0110)  # 6
        original_id = id(bm)
        bm |= 0b1010  # 10
        assert id(bm) == original_id
        assert bm.value == 0b1110  # 14

        bm = BitMask(4, 0b0110)
        bm2 = BitMask(4, 0b0001)  # 1
        original_id = id(bm)
        bm |= bm2
        assert id(bm) == original_id
        assert bm.value == 0b0111  # 7

    def test_ixor(self):
        bm = BitMask(4, 0b0110)  # 6
        original_id = id(bm)
        bm ^= 0b0010  # 2
        assert id(bm) == original_id
        assert bm.value == 0b0100  # 4

        bm = BitMask(4, 0b0110)
        bm2 = BitMask(4, 0b1101)  # 13
        original_id = id(bm)
        bm ^= bm2
        assert id(bm) == original_id
        assert bm.value == 0b1011  # 11

    def test_in_place_bitwise_ops_errors(self):
        bm = BitMask(8)
        with pytest.raises(ValueError):
            bm &= 256
        with pytest.raises(TypeError):
            bm |= BitMask(7)
        with pytest.raises(TypeError):
            bm ^= "string"

    def test_ilshift(self):
        bm = BitMask(4, 0b0001)  # 1
        original_id = id(bm)
        bm <<= 1
        assert id(bm) == original_id
        assert bm.value == 0b0010  # 2

        bm = BitMask(4, 0b1000)  # 8
        bm <<= 1  # Shift out of bounds (for 4-bit)
        assert bm.value == 0b0000  # 0

    def test_irshift(self):
        bm = BitMask(4, 0b1000)  # 8
        original_id = id(bm)
        bm >>= 1
        assert id(bm) == original_id
        assert bm.value == 0b0100  # 4

        bm = BitMask(4, 0b0001)  # 1
        bm >>= 1
        assert bm.value == 0b0000  # 0

    def test_in_place_shift_ops_errors(self):
        bm = BitMask(8)
        with pytest.raises(ValueError):
            bm <<= -1
        with pytest.raises(ValueError):
            bm >>= -1
        with pytest.raises(ValueError):
            bm <<= (_MAX_BITMASK_LENGTH + 1)
        with pytest.raises(TypeError):
            bm <<= "string"

    def test_bool(self):
        assert bool(BitMask(4, 0)) is False
        assert bool(BitMask(4, 1)) is True
        assert bool(BitMask(8, 255)) is True

    def test_int(self):
        assert int(BitMask(4, 10)) == 10
        assert int(BitMask(8, 0)) == 0
        assert int(BitMask(1, 1)) == 1

    def test_float(self):
        assert float(BitMask(4, 10)) == 10.0
        assert float(BitMask(8, 0)) == 0.0
        assert float(BitMask(1, 1)) == 1.0
