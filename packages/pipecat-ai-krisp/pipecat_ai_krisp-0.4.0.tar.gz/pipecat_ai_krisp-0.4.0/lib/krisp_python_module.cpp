// This class was created based on the example provided in:
// https://github.com/krispai/Krisp-SDK-Sample-Apps/blob/krisp-sdk-v9/src/sample-python/krisp_python_module.cpp
// Modifications have been made to adapt it for working with the new methods, while retaining
// key functionalities from the original implementation.
#include <string>
#include <memory>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include <krisp-audio-sdk-nc.hpp>

namespace py = pybind11;

static KrispAudioSamplingRate getKrispSamplingRate(unsigned rate) {
    switch (rate) {
        case 8000: return KRISP_AUDIO_SAMPLING_RATE_8000HZ;
        case 16000: return KRISP_AUDIO_SAMPLING_RATE_16000HZ;
        case 32000: return KRISP_AUDIO_SAMPLING_RATE_32000HZ;
        case 44100: return KRISP_AUDIO_SAMPLING_RATE_44100HZ;
        case 48000: return KRISP_AUDIO_SAMPLING_RATE_48000HZ;
        case 88200: return KRISP_AUDIO_SAMPLING_RATE_88200HZ;
        case 96000: return KRISP_AUDIO_SAMPLING_RATE_96000HZ;
        default: throw std::runtime_error("Unsupported sample rate: " + std::to_string(rate));
    }
}

template<typename SamplingFormat>
class KrispAudioProcessorTemplate {
public:
    KrispAudioProcessorTemplate(unsigned sampleRate, const std::wstring &modelPath)
        : _sampleRate(sampleRate), _channels(1), _modelPath(modelPath) {

        if (krispAudioGlobalInit(nullptr) != 0) {
            throw std::runtime_error("Failed to initialize Krisp SDK");
        }

        if (krispAudioSetModel(_modelPath.c_str(), "myModelName") != 0) {
            krispAudioGlobalDestroy();
            throw std::runtime_error("Error loading AI model");
        }

        reset_audio_session();

        unsigned samplesPerFrame = (_sampleRate * _frameSize) / 1000;
        unsigned frameLength = samplesPerFrame * _channels;
        _frameBuffer.resize(frameLength);
    }

    ~KrispAudioProcessorTemplate() {
        if (krispAudioRemoveModel("myModelName") != 0) {
            // Log or handle model removal error
        }
        if (krispAudioGlobalDestroy() != 0) {
            // Log or handle global destruction error
        }
    }

    void reset_audio_session() {
        if (_sessionId) {
            if (krispAudioNcCloseSession(_sessionId) != 0) {
                // Log or handle session closure error
            }
            _sessionId = nullptr;
        }

        auto inRate = getKrispSamplingRate(_sampleRate);
        auto outRate = inRate;
        constexpr KrispAudioFrameDuration krispFrameDuration = KRISP_AUDIO_FRAME_DURATION_10MS;

        _sessionId = krispAudioNcCreateSession(inRate, outRate, krispFrameDuration, "myModelName");
        if (!_sessionId) {
            throw std::runtime_error("Error creating session");
        }
    }

    void add_audio_frames(const py::array_t<SamplingFormat> &audio_frames) {
        py::buffer_info info = audio_frames.request();
        const SamplingFormat *chunk_ptr = static_cast<const SamplingFormat *>(info.ptr);
        size_t chunk_size = static_cast<size_t>(info.size);

        _audio_data.resize(chunk_size + _remainderSampleCount);
        std::memcpy(_audio_data.data() + _remainderSampleCount,
                    chunk_ptr, chunk_size * sizeof(SamplingFormat));

        _remainderSampleCount = 0;
    }

    [[nodiscard]] size_t get_samples_count() const {
        return _audio_data.size();
    }

    unsigned get_processed_frames(py::array_t<SamplingFormat> &python_output_frames) {
        unsigned samplesPerFrame = (_sampleRate * _frameSize) / 1000;
        unsigned frameLength = samplesPerFrame * _channels;

        py::buffer_info buf_info = python_output_frames.request();
        auto *output_ptr = reinterpret_cast<SamplingFormat *>(buf_info.ptr);
        size_t buffer_frame_count = static_cast<size_t>(buf_info.size) / frameLength;
        size_t audio_frame_count = _audio_data.size() / frameLength;

        if (buffer_frame_count < audio_frame_count) {
            throw std::runtime_error("Buffer is too small for the given audio data");
        }

        _remainderSampleCount = _audio_data.size() % frameLength;

        unsigned processed_frames = 0;
        auto frame_start_it = _audio_data.begin();
        auto frame_end_it = _audio_data.begin();

        std::vector<float> floatInputBuffer(frameLength); // Temporary buffer for Krisp input
        std::vector<float> floatOutputBuffer(frameLength); // Temporary buffer for Krisp output

        for (unsigned i = 0; i < audio_frame_count; ++i) {
            std::advance(frame_end_it, frameLength);

            // Convert input data to float
            if constexpr (std::is_same<SamplingFormat, int16_t>::value) {
                std::transform(frame_start_it, frame_end_it, floatInputBuffer.begin(),
                               [](int16_t sample) { return static_cast<float>(sample) / 32768.0f; });
            } else if constexpr (std::is_same<SamplingFormat, float>::value) {
                std::copy(frame_start_it, frame_end_it, floatInputBuffer.begin());
            } else {
                throw std::runtime_error("Unsupported audio format");
            }

            // Process with Krisp
            int result = krispAudioNcCleanAmbientNoiseFloat(
                _sessionId, floatInputBuffer.data(), frameLength, floatOutputBuffer.data(), frameLength);

            if (result != 0) {
                throw std::runtime_error("Error processing audio");
            }

            // Convert Krisp output back to the original format
            if constexpr (std::is_same<SamplingFormat, int16_t>::value) {
                std::transform(floatOutputBuffer.begin(), floatOutputBuffer.end(),
                               output_ptr + i * frameLength,
                               [](float sample) {
                                   sample = std::clamp(sample, -1.0f, 1.0f); // Ensure it's in the valid range
                                   return static_cast<int16_t>(sample * 32768.0f);
                               });
            } else if constexpr (std::is_same<SamplingFormat, float>::value) {
                std::copy(floatOutputBuffer.begin(), floatOutputBuffer.end(), output_ptr + i * frameLength);
            }

            frame_start_it = frame_end_it;
            ++processed_frames;
        }

        if (_remainderSampleCount) {
            std::copy(frame_end_it, frame_end_it + static_cast<long>(_remainderSampleCount), _audio_data.begin());
        }

        return processed_frames;
    }

private:
    const unsigned _frameSize = 10;
    unsigned _sampleRate;
    unsigned _channels;
    unsigned long _remainderSampleCount = 0;
    std::vector<SamplingFormat> _audio_data;
    std::vector<SamplingFormat> _frameBuffer;
    std::wstring _modelPath;
    KrispAudioSessionID _sessionId = nullptr;
};

typedef KrispAudioProcessorTemplate<float> KrispAudioProcessorPcmFloat;
typedef KrispAudioProcessorTemplate<int16_t> KrispAudioProcessorPcm16;

PYBIND11_MODULE(krisp_python, m) {
    py::class_<KrispAudioProcessorPcmFloat>(m, "KrispAudioProcessorPcmFloat")
            .def(py::init<unsigned, std::wstring>())
            .def("add_audio_frames", &KrispAudioProcessorPcmFloat::add_audio_frames)
            .def("get_processed_frames", &KrispAudioProcessorPcmFloat::get_processed_frames)
            .def("get_samples_count", &KrispAudioProcessorPcmFloat::get_samples_count);

    py::class_<KrispAudioProcessorPcm16>(m, "KrispAudioProcessorPcm16")
            .def(py::init<unsigned, std::wstring>())
            .def("add_audio_frames", &KrispAudioProcessorPcm16::add_audio_frames)
            .def("get_processed_frames", &KrispAudioProcessorPcm16::get_processed_frames)
            .def("get_samples_count", &KrispAudioProcessorPcm16::get_samples_count);
}
