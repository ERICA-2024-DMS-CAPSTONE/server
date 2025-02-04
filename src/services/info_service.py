from protos import Service_pb2
from common.state import State


class InfoService:
    def fetch_info(self):
        state = State()
        while True:
            yield Service_pb2.Info(
                attention=Service_pb2.AttentionInfo(
                    level=state.attention,
                    minLevel=state.attentionMinLevel,
                    maxLevel=state.attentionMaxLevel,
                ),
                speaker=Service_pb2.SpeakerInfo(
                    isMuted=state.isMuted,
                    level=state.soundLevel,
                ),
                temperature=Service_pb2.TemperatureInfo(
                    car=state.carTemp,
                    driver=state.driverTemp,
                    passenger=state.passengerTemp,
                    carAverage=state.carAverageTemp,
                    driverAverage=state.driverAverageTemp,
                    passengerAverage=state.passengerAverageTemp,
                )
            )

    def update_info(self, request):
        state = State()
        state.attention = request.attention.level
        state.attentionMinLevel = request.attention.minLevel
        state.attentionMaxLevel = request.attention.maxLevel
        state.isMuted = request.speaker.isMuted
        state.soundLevel = request.speaker.level
        state.carTemp = request.temperature.car
        state.driverTemp = request.temperature.driver
        state.passengerTemp = request.temperature.passenger
        state.carAverageTemp = request.temperature.carAverage
        state.driverAverageTemp = request.temperature.driverAverage
        state.passengerAverageTemp = request.temperature.passengerAverage

    def offer(self, request):
        return Service_pb2.MirrorInfo(sdp=request.sdp, type=request.type)
